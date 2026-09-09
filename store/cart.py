from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, size='M', override_quantity=False):
        item_key = f"{product.id}_{size}"
        if item_key not in self.cart:
            self.cart[item_key] = {
                'product_id': product.id,
                'quantity': 0,
                'price': str(product.price),
                'size': size
            }
        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item_key):
        item_key = str(item_key)
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()
        else:
            removed = False
            for k in list(self.cart.keys()):
                if k == item_key or k.startswith(f"{item_key}_"):
                    del self.cart[k]
                    removed = True
            if removed:
                self.save()

    def __iter__(self):
        cart = self.cart.copy()
        product_ids = []
        for key, item in cart.items():
            if isinstance(item, dict):
                pid = item.get('product_id')
                if not pid:
                    try:
                        pid = int(str(key).split('_')[0])
                        item['product_id'] = pid
                        item['size'] = item.get('size', 'M')
                    except (ValueError, IndexError):
                        continue
                product_ids.append(pid)

        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}

        for key, item in list(cart.items()):
            if not isinstance(item, dict):
                continue
            pid = item.get('product_id')
            if not pid:
                try:
                    pid = int(str(key).split('_')[0])
                except (ValueError, IndexError):
                    continue
            product = products.get(pid)
            if product:
                item_copy = item.copy()
                item_copy['product'] = product
                item_copy['item_key'] = key
                item_copy['size'] = item.get('size', 'M')
                item_copy['price'] = Decimal(str(item.get('price', product.price)))
                item_copy['total_price'] = (item_copy['price'] * Decimal(str(item.get('quantity', 1)))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                yield item_copy

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values() if isinstance(item, dict))

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self.cart.values():
            if isinstance(item, dict):
                try:
                    price = Decimal(str(item.get('price', 0)))
                    qty = Decimal(str(item.get('quantity', 0)))
                    total += price * qty
                except Exception:
                    pass
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def coupon(self):
        coupon_id = self.session.get('coupon_id')
        if coupon_id:
            from .models import Coupon
            return Coupon.objects.filter(id=coupon_id, active=True).first()
        return None

    def get_discount(self):
        if self.coupon:
            return (self.get_total_price() * (Decimal(str(self.coupon.discount_percent)) / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')

    def get_total_price_after_discount(self):
        total = self.get_total_price() - self.get_discount()
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def get_free_shipping_needed(self):
        total = self.get_total_price()
        threshold = Decimal('999.00')
        if total >= threshold:
            return Decimal('0.00')
        return (threshold - total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def get_free_shipping_percent(self):
        total = self.get_total_price()
        threshold = Decimal('999.00')
        if threshold <= Decimal('0.00'):
            return 100
        return min(int((total / threshold) * 100), 100)

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()
