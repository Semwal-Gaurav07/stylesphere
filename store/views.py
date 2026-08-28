from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count, Avg
from decimal import Decimal
from datetime import datetime, timedelta
from .models import Category, Product, Order, OrderItem, Coupon, Review, Wishlist
from accounts.models import Profile
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, CouponApplyForm, ReviewForm
from .utils import check_pincode_serviceability, generate_admin_whatsapp_url

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    trending_products = Product.objects.filter(available=True)[:6]

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
        'trending_products': trending_products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'user_wishlist_ids': user_wishlist_ids
    })

def product_detail(request, id=None, slug=None):
    product = None
    if id and slug:
        product = Product.objects.filter(id=id, slug=slug, available=True).first()
    if not product and slug:
        product = Product.objects.filter(slug=slug, available=True).first()
    if not product and id:
        product = Product.objects.filter(id=id, available=True).first()
    if not product:
        product = get_object_or_404(Product, available=True)

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    reviews = product.reviews.all()
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    delivery_date = (datetime.now() + timedelta(days=3)).strftime("%A, %b %d")

    return render(request, 'store/product/detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_product_form': cart_product_form,
        'review_form': review_form,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
        'delivery_date': delivery_date
    })

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', 'M')
    override = request.POST.get('override') == 'True'
    buy_now = request.POST.get('buy_now') == 'true'

    cart.add(product=product, quantity=quantity, size=size, override_quantity=override)

    if buy_now:
        return redirect('store:order_create')
    return redirect('store:cart_detail')

@require_POST
def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
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

def pincode_check(request):
    pincode = request.GET.get('pincode', '')
    res = check_pincode_serviceability(pincode)
    return JsonResponse(res)

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store:product_list')

    if not request.user.is_authenticated:
        messages.info(request, 'Please create an account or sign in to complete your order.')
        return redirect('/accounts/register/?next=/orders/create/')

    profile, _ = Profile.objects.get_or_create(user=request.user)
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'address': profile.address,
        'city': profile.city,
        'postal_code': profile.postal_code,
    }

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
            order.phone_number = request.POST.get('phone_number', profile.phone_number or '')
            order.save()

            if not profile.address:
                profile.address = order.address
                profile.city = order.city
                profile.postal_code = order.postal_code
                profile.phone_number = order.phone_number
                profile.save()

            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity'],
                    size=item['size']
                )
                if product.stock >= item['quantity']:
                    product.stock -= item['quantity']
                    product.save()

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

@login_required
def order_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/orders/invoice.html', {'order': order})

@login_required
def admin_analytics(request):
    """
    Staff / Admin Revenue & Sales Analytics Dashboard
    """
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Admin access required to view business analytics.')
        return redirect('store:product_list')

    total_orders = Order.objects.count()
    paid_orders = Order.objects.filter(paid=True).count()
    cod_orders = Order.objects.filter(payment_method__icontains='COD').count()
    
    total_revenue = sum(o.get_total_cost() for o in Order.objects.all())
    paid_revenue = sum(o.get_total_cost() for o in Order.objects.filter(paid=True))

    recent_orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created')[:8]
    low_stock_products = Product.objects.filter(stock__lte=3).order_by('stock')

    # Top selling sizes
    size_breakdown = OrderItem.objects.values('size').annotate(total_qty=Sum('quantity')).order_by('-total_qty')

    # Status Breakdown
    status_counts = Order.objects.values('status').annotate(count=Count('id'))

    return render(request, 'store/admin/analytics.html', {
        'total_orders': total_orders,
        'paid_orders': paid_orders,
        'cod_orders': cod_orders,
        'total_revenue': total_revenue,
        'paid_revenue': paid_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'size_breakdown': size_breakdown,
        'status_counts': status_counts,
    })
