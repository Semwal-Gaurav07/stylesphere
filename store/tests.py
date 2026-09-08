from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Category, Product, ProductVariant, Order, OrderItem
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
        self.variant = ProductVariant.objects.create(
            product=self.product,
            size='L',
            stock=5
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
        self.assertEqual(self.product.get_stock_for_size('M'), 15)

    def test_provenance_vault_view(self):
        response = self.client.get(reverse('store:provenance_vault'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Certificate of Provenance')

    def test_midnight_vault_locked_view(self):
        response = self.client.get(reverse('store:midnight_vault'))
        self.assertEqual(response.status_code, 200)
