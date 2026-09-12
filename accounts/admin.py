from django.contrib import admin
from .models import Profile, PasswordResetOTP

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'postal_code']
    search_fields = ['user__username', 'user__email', 'phone_number', 'city']

@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'is_verified', 'attempts']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
