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
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        cart = self.cart.copy()
        product_ids = [item['product_id'] for item in cart.values()]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}

        for key, item in cart.items():
            item['product'] = products.get(item['product_id'])
            item['item_key'] = key
            item['price'] = Decimal(item['price'])
            item['total_price'] = int(item['price'] * item['quantity'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(int(Decimal(item['price']) * item['quantity']) for item in self.cart.values())

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
        del self.session[settings.CART_SESSION_ID]
        self.save()