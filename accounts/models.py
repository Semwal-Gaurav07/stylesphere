from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        now = timezone.now()
        return not self.is_verified and (now - self.created_at) < timedelta(minutes=10) and self.attempts < 5

    @classmethod
    def create_otp(cls, user):
        # Invalidate previous unverified OTPs for this user
        cls.objects.filter(user=user, is_verified=False).delete()
        code = f"{random.randint(100000, 999999)}"
        return cls.objects.create(user=user, otp_code=code)

    def __str__(self):
        return f"OTP for {self.user.username} (Code: {self.otp_code})"
