from .utils import check_pincode_serviceability, generate_admin_whatsapp_url
from django.http import JsonResponse
from .notifications import send_order_confirmation_email
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import F, Q, Sum, Count, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from decimal import Decimal
from datetime import datetime, timedelta
import random
from .models import Category, Product, ProductImage, Order, OrderItem, Coupon, Review, Wishlist
from accounts.models import Profile
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, CouponApplyForm, ReviewForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category').prefetch_related('images', 'variants', 'reviews').order_by('-created')
    trending_products = Product.objects.filter(available=True).select_related('category').prefetch_related('images')[:6]

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(print_type__icontains=query) |
            Q(fit_type__icontains=query)
        )

    print_filter = request.GET.get('print_type')
    if print_filter:
        products = products.filter(print_type__icontains=print_filter)

    fit_filter = request.GET.get('fit_type')
    if fit_filter:
        products = products.filter(fit_type__icontains=fit_filter)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except Exception:
            pass

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

    # Annotate with average user rating for rating filter & ranking
    products = products.annotate(avg_rating=Avg('reviews__rating'))

    rating_filter = request.GET.get('rating')
    if rating_filter:
        try:
            products = products.filter(avg_rating__gte=float(rating_filter))
        except (ValueError, TypeError):
            pass

    # 4 Unique Flagship Spotlight Editions for the Top Banner
    spotlight_products = Product.objects.filter(available=True).order_by('-created')[:4]

    # Pagination: 9 products per page (matches clean 3x3 layout)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'store/product/list.html', {
        'category': category,
        'categories': categories,
        'products': page_obj,
        'page_obj': page_obj,
        'trending_products': trending_products,
        'spotlight_products': spotlight_products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'rating_filter': rating_filter,
        'print_filter': print_filter,
        'fit_filter': fit_filter,
        'user_wishlist_ids': user_wishlist_ids
    })

def product_detail(request, id, slug):
    product = Product.objects.filter(id=id, slug=slug, available=True).first()
    if not product:
        product = Product.objects.filter(slug=slug, available=True).first()
    if not product:
        product = get_object_or_404(Product, id=id, available=True)

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    reviews = product.reviews.all()
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    gallery_images = product.get_gallery_images()
    delivery_date = (datetime.now() + timedelta(days=3)).strftime("%A, %b %d")

    return render(request, 'store/product/detail.html', {
        'product': product,
        'gallery_images': gallery_images,
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
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    size = request.POST.get('size', 'M')
    override = request.POST.get('override') == 'True'
    buy_now = request.POST.get('buy_now') == 'true'

    # Inventory & Per-Size Variant Out-of-Stock Guard
    size_stock = product.get_stock_for_size(size)
    if size_stock <= 0 or not product.available:
        messages.error(request, f'Sorry, size {size} of "{product.name}" is currently sold out.')
        return redirect(product.get_absolute_url())

    if quantity > size_stock:
        quantity = size_stock
        messages.warning(request, f'Adjusted to maximum available atelier inventory for size {size} ({size_stock} pieces).')

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
        cart = Cart(request)
        cart_total = cart.get_total_price()
        coupon = Coupon.objects.filter(code__iexact=code).first()
        if coupon:
            is_valid, msg = coupon.is_valid(cart_total)
            if is_valid:
                request.session['coupon_id'] = coupon.id
                messages.success(request, f'Coupon "{coupon.code}" applied! You get {coupon.discount_percent}% off your order.')
            else:
                request.session['coupon_id'] = None
                messages.error(request, msg)
        else:
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
        messages.success(request, 'Your t-shirt review has been submitted!')
    return redirect(product.get_absolute_url())

@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.info(request, f'Removed "{product.name}" from your Wishlist.')
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f'Added "{product.name}" to your Wishlist!')
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
        messages.info(request, 'Please sign in or create an account to complete your printed t-shirt order.')
        return redirect('/accounts/register/?next=/orders/create/')

    profile, _ = Profile.objects.get_or_create(user=request.user)
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone_number': profile.phone_number,
        'address': profile.address,
        'city': profile.city,
        'postal_code': profile.postal_code,
    }

    coupon_id = request.session.get('coupon_id')
    discount = 0
    coupon = None
    if coupon_id:
        coupon = Coupon.objects.filter(id=coupon_id, active=True).first()
        if coupon:
            is_valid, _ = coupon.is_valid(cart.get_total_price())
            if is_valid:
                discount = coupon.discount_percent
            else:
                coupon = None
                request.session['coupon_id'] = None
        else:
            request.session['coupon_id'] = None

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.discount = discount
                order.awb_code = f"SS-EXP-{random.randint(100000, 999999)}"
                order.tracking_number = order.awb_code
                order.save()

                if coupon:
                    Coupon.objects.filter(id=coupon.id).update(used_count=F('used_count') + 1)

                if not profile.address:
                    profile.address = order.address
                    profile.city = order.city
                    profile.postal_code = order.postal_code
                if not profile.phone_number and order.phone_number:
                    profile.phone_number = order.phone_number
                profile.save()

                from django.db.models import F
                insufficient_stock = False

                for item in cart:
                    product = item['product']
                    qty = item['quantity']

                    # Atomic stock decrement: Deduct per-size variant stock if configured, else global stock
                    size_variant = product.variants.filter(size=item['size']).first()
                    if size_variant:
                        rows_updated = product.variants.filter(
                            id=size_variant.id,
                            stock__gte=qty
                        ).update(stock=F('stock') - qty)
                        # Also sync global counter
                        Product.objects.filter(id=product.id).update(stock=F('stock') - qty)
                    else:
                        rows_updated = Product.objects.filter(
                            id=product.id,
                            stock__gte=qty,
                            available=True
                        ).update(stock=F('stock') - qty)

                    if not rows_updated:
                        messages.error(request, f'Sorry, size {item["size"]} of "{product.name}" has insufficient inventory ({qty} requested).')
                        insufficient_stock = True
                        transaction.set_rollback(True)
                        break

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        quantity=qty,
                        size=item['size']
                    )

                if insufficient_stock:
                    return redirect('store:cart_detail')

                cart.clear()
                request.session['coupon_id'] = None
                request.session['order_id'] = order.id
                # Customer proceeds to select payment method (COD or GPay)
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
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/orders/invoice.html', {'order': order})

@user_passes_test(lambda u: u.is_staff)
def admin_analytics(request):
    from django.contrib.auth.models import User
    total_users = User.objects.count()
    all_users = User.objects.all().order_by('-date_joined')
    total_orders = Order.objects.count()
    revenue_agg = OrderItem.objects.filter(order__paid=True).aggregate(
        rev=Sum(F('price') * F('quantity'))
    )
    total_revenue = revenue_agg['rev'] or Decimal('0.00')
    paid_orders = Order.objects.filter(paid=True).count()
    cod_orders = Order.objects.filter(payment_method__icontains='COD').count()
    low_stock_products = Product.objects.filter(stock__lte=3)
    
    top_selling_sizes = OrderItem.objects.values('size').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:5]
    top_cities = Order.objects.values('city').annotate(order_count=Count('id')).order_by('-order_count')[:5]

    return render(request, 'store/admin_analytics.html', {
        'total_users': total_users,
        'all_users': all_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'paid_orders': paid_orders,
        'cod_orders': cod_orders,
        'low_stock_products': low_stock_products,
        'top_selling_sizes': top_selling_sizes,
        'top_cities': top_cities,
    })

def shipping_policy(request):
    return render(request, 'store/policies/shipping.html')

def returns_policy(request):
    return render(request, 'store/policies/returns.html')

def privacy_policy(request):
    return render(request, 'store/policies/privacy.html')

def terms_of_service(request):
    return render(request, 'store/policies/terms.html')


def provenance_vault(request):
    """
    Digital Provenance Vault & Holographic Certificate of Authenticity.
    """
    awb = request.GET.get('awb', '').strip()
    order = None
    if awb:
        order = Order.objects.filter(awb_code__iexact=awb).first() or                 Order.objects.filter(tracking_number__iexact=awb).first()
        if not order and awb.isdigit():
            order = Order.objects.filter(id=int(awb)).first()

    if order:
        cert_serial = f"ATELIER-{order.created.year}-{order.id:04d}"
        if request.user.is_authenticated and (request.user.is_staff or request.user == order.user):
            cert_owner = f"{order.first_name} {order.last_name}"
        else:
            fn = order.first_name
            ln = order.last_name
            masked_fn = (fn[0] + "*" * (len(fn) - 1)) if len(fn) > 1 else (fn + "*")
            masked_ln = (ln[0] + "*" * (len(ln) - 1)) if len(ln) > 1 else (ln + "*")
            cert_owner = f"{masked_fn} {masked_ln} (Verified Client)"
        cert_fabric = "240+ GSM Combed French Terry Cotton"
        cert_awb = order.awb_code or f"SS-EXP-{order.id}"
        cert_date = order.created.strftime('%d %B %Y')
    else:
        cert_serial = "ATELIER-2026-0042 // SER-01"
        cert_owner = "Client Privilege Registered"
        cert_fabric = "240+ GSM Bio-Washed French Terry"
        cert_awb = awb or "SS-EXP-2026-ATELIER"
        cert_date = datetime.now().strftime('%d %B %Y')

    return render(request, 'store/vault/provenance.html', {
        'search_query': awb,
        'order': order,
        'cert_serial': cert_serial,
        'cert_owner': cert_owner,
        'cert_fabric': cert_fabric,
        'cert_awb': cert_awb,
        'cert_date': cert_date,
    })

def midnight_vault(request):
    """
    The Midnight Vault: Exclusive password-protected and curfew-based VIP drops.
    """
    if request.GET.get('lock'):
        request.session['vault_unlocked'] = False
        return redirect('store:midnight_vault')

    from django.utils import timezone
    local_now = timezone.localtime(timezone.now())
    now_hour = local_now.hour
    is_curfew = (now_hour >= 23 or now_hour < 1)
    is_unlocked = request.session.get('vault_unlocked', False) or is_curfew

    if request.method == 'POST':
        passkey = request.POST.get('passkey', '').strip().upper()
        if passkey in ['STYLE2026', 'ATELIER', 'VIP2026', 'VAULT20']:
            request.session['vault_unlocked'] = True
            is_unlocked = True
            messages.success(request, 'VIP Atelier Access Granted. Welcome to the Vault.')
        else:
            messages.error(request, 'Invalid Atelier Passkey. Access Denied.')

    vault_products = Product.objects.filter(available=True).order_by('-created')[:6]

    return render(request, 'store/vault/midnight_vault.html', {
        'is_unlocked': is_unlocked,
        'vault_products': vault_products
    })

def check_pincode_view(request):
    """
    API endpoint for checking delivery estimates and COD availability by Indian pincode.
    """
    pincode = request.GET.get('pincode', '')
    data = check_pincode_serviceability(pincode)
    return JsonResponse(data)


@login_required
@require_POST
def order_cancel(request, order_id):
    """
    Allows clients or staff to cancel placed/processing orders and safely restore inventory.
    """
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ['Shipped', 'Delivered']:
        messages.error(request, f'Order #{order.id} cannot be cancelled because it has already been {order.status.lower()}.')
        return redirect('accounts:profile')

    if order.status == 'Cancelled':
        messages.info(request, f'Order #{order.id} is already cancelled.')
        return redirect('accounts:profile')

    from django.db.models import F
    with transaction.atomic():
        # Restore stock for each item
        for item in order.items.all():
            variant = item.product.variants.filter(size=item.size).first()
            if variant:
                variant.stock = F('stock') + item.quantity
                variant.save()
            Product.objects.filter(id=item.product.id).update(stock=F('stock') + item.quantity)
            Product.objects.filter(id=item.product.id, available=False).update(available=True)

        order.status = 'Cancelled'
        order.save()

    messages.success(request, f'Order #{order.id} has been cancelled successfully, and reserved inventory was returned.')
    return redirect('accounts:profile')
