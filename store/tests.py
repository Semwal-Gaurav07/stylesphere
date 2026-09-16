from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Category, Product, ProductVariant, Order, OrderItem, Coupon
from .cart import Cart

class StoreCatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Streetwear', slug='streetwear')
        self.product = Product.objects.create(
            category=self.category,
            name='Akira Neo-Tokyo Tee',
            slug='akira-neo-tokyo-tee',
            price=Decimal('1299.00'),
            stock=15,
            available=True
        )
        self.variant, _ = ProductVariant.objects.update_or_create(
            product=self.product,
            size='L',
            defaults={'stock': 5}
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Akira Neo-Tokyo Tee')

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', args=[self.product.id, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Akira Neo-Tokyo Tee')

    def test_variant_stock_lookup(self):
        self.assertEqual(self.product.get_stock_for_size('L'), 5)
        # Size without specific variant falls back to global product stock
        self.assertEqual(self.product.get_stock_for_size('3XL'), 15)

    def test_provenance_vault_view(self):
        response = self.client.get(reverse('store:provenance_vault'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Certificate of Provenance')

    def test_midnight_vault_locked_view(self):
        response = self.client.get(reverse('store:midnight_vault'))
        self.assertEqual(response.status_code, 200)

    def test_pincode_check_api(self):
        response = self.client.get(reverse('store:check_pincode') + '?pincode=134113')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['valid'])
        self.assertTrue(data['cod_available'])

    def test_coupon_min_purchase_validation(self):
        coupon = Coupon.objects.create(
            code='SAVE20',
            discount_percent=20,
            active=True,
            min_purchase=Decimal('1000.00'),
            max_uses=100
        )
        # Empty / below threshold should fail
        is_valid, msg = coupon.is_valid(Decimal('0.00'))
        self.assertFalse(is_valid)
        is_valid, msg = coupon.is_valid(Decimal('500.00'))
        self.assertFalse(is_valid)
        # Above threshold should pass
        is_valid, msg = coupon.is_valid(Decimal('1200.00'))
        self.assertTrue(is_valid)

    def test_order_cancellation_restores_stock(self):
        user = User.objects.create_user(username='buyer', email='buyer@example.com', password='Pass123!45')
        self.client.force_login(user)
        order = Order.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            email='buyer@example.com',
            phone_number='9876543210',
            address='123 Fashion Street',
            postal_code='134113',
            city='Panchkula',
            status='Placed'
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            price=self.product.price,
            quantity=2,
            size='L'
        )
        # Simulate stock deduction
        ProductVariant.objects.filter(id=self.variant.id).update(stock=3)
        Product.objects.filter(id=self.product.id).update(stock=13)

        # Cancel order
        response = self.client.post(reverse('store:order_cancel', args=[order.id]))
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'Cancelled')
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock, 5)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 15)
