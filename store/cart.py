from decimal import Decimal
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
                item_copy['price'] = Decimal(item.get('price', product.price))
                item_copy['total_price'] = int(item_copy['price'] * item.get('quantity', 1))
                yield item_copy

    def __len__(self):
        return sum(item.get('quantity', 0) for item in self.cart.values() if isinstance(item, dict))

    def get_total_price(self):
        total = 0
        for item in self.cart.values():
            if isinstance(item, dict):
                try:
                    total += int(Decimal(item.get('price', 0)) * item.get('quantity', 0))
                except Exception:
                    pass
        return total

    def get_free_shipping_needed(self):
        total = self.get_total_price()
        threshold = 999
        if total >= threshold:
            return 0
        return threshold - total

    def get_free_shipping_percent(self):
        total = self.get_total_price()
        threshold = 999
        return min(int((total / threshold) * 100), 100)

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()
