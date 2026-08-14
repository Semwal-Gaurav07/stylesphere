from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from .models import Category, Product, OrderItem, Coupon, Review, Wishlist
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, CouponApplyForm, ReviewForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created')

    user_wishlist_ids = []
    if request.user.is_authenticated:
        user_wishlist_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    return render(request, 'store/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'user_wishlist_ids': user_wishlist_ids
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    reviews = product.reviews.all()
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    return render(request, 'store/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'review_form': review_form,
        'reviews': reviews,
        'in_wishlist': in_wishlist
    })

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('store:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    coupon_apply_form = CouponApplyForm()
    coupon_id = request.session.get('coupon_id')
    coupon = None
    discount = 0
    if coupon_id:
        coupon = Coupon.objects.filter(id=coupon_id).first()
        if coupon:
            discount = coupon.discount_percent

    return render(request, 'store/cart/detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
        'coupon': coupon,
        'discount': discount
    })

@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code'].strip().upper()
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, f'Coupon "{coupon.code}" applied! You get {coupon.discount_percent}% off.')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'Invalid or expired promo code.')
    return redirect('store:cart_detail')

@login_required
@require_POST
def review_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        messages.success(request, 'Your review has been submitted!')
    return redirect(product.get_absolute_url())

@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.info(request, f'Removed {product.name} from your Wishlist.')
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f'Added {product.name} to your Wishlist!')
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))

@login_required
def wishlist_detail(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist/detail.html', {'wishlist_items': wishlist_items})

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store:product_list')

    if not request.user.is_authenticated:
        messages.info(request, 'Please create an account or sign in to complete your order.')
        return redirect('/accounts/register/?next=/orders/create/')

    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    if hasattr(request.user, 'profile'):
        initial_data.update({
            'address': request.user.profile.address,
            'city': request.user.profile.city,
            'postal_code': request.user.profile.postal_code,
        })

    coupon_id = request.session.get('coupon_id')
    discount = 0
    if coupon_id:
        coupon = Coupon.objects.filter(id=coupon_id).first()
        if coupon:
            discount = coupon.discount_percent

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.discount = discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            request.session['coupon_id'] = None
            request.session['order_id'] = order.id
            return redirect('payment:process')
    else:
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'store/orders/create.html', {
        'cart': cart,
        'form': form,
        'discount': discount
    })