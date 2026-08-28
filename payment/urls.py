from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/razorpay/', views.razorpay_webhook, name='razorpay_webhook'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
