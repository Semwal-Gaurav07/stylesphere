from django.test import TestCase, Client
from django.urls import reverse
from store.models import Order
from decimal import Decimal

class PaymentFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            first_name='Gaurav',
            last_name='Semwal',
            email='gaurav@example.com',
            address='Atelier Studio',
            postal_code='134113',
            city='Panchkula'
        )

    def test_payment_process_requires_order_session(self):
        response = self.client.get(reverse('payment:process'))
        self.assertEqual(response.status_code, 302)

    def test_webhook_rejects_get(self):
        response = self.client.get(reverse('payment:webhook'))
        self.assertEqual(response.status_code, 405)
