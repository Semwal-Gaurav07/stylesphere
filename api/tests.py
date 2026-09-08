from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from store.models import Category, Product, Wishlist
from decimal import Decimal

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', email='api@example.com', password='ApiPassword123!')
        self.category = Category.objects.create(name='Anime', slug='anime')
        self.product = Product.objects.create(
            category=self.category,
            name='Berserk Tee',
            slug='berserk-tee',
            price=Decimal('1499.00'),
            stock=10,
            available=True
        )

    def test_products_endpoint(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)

    def test_wishlist_authenticated_creation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/wishlist/', {'product_id': self.product.id})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_order_creation_requires_auth(self):
        response = self.client.post('/api/orders/', {'first_name': 'Test'})
        self.assertEqual(response.status_code, 401)
