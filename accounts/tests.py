from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PasswordResetOTP

class AccountsAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testclient', email='client@example.com', password='TestPassword123!')

    def test_login_page_renders(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_otp_generation(self):
        otp = PasswordResetOTP.create_otp(self.user)
        self.assertEqual(len(otp.otp_code), 6)
        self.assertTrue(otp.otp_code.isdigit())
        self.assertTrue(otp.is_valid())
        self.assertFalse(otp.is_verified)
