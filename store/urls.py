from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.review_add, name='review_add'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<str:item_key>/', views.cart_remove, name='cart_remove'),
    path('coupon/apply/', views.coupon_apply, name='coupon_apply'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/invoice/', views.order_invoice, name='order_invoice'),
    path('analytics/', views.admin_analytics, name='admin_analytics'),
    path('provenance/', views.provenance_vault, name='provenance_vault'),
    path('vault/', views.midnight_vault, name='midnight_vault'),

    # Compliance & Trust Policies
    path('policies/shipping/', views.shipping_policy, name='shipping_policy'),
    path('policies/returns/', views.returns_policy, name='returns_policy'),
    path('policies/privacy/', views.privacy_policy, name='privacy_policy'),
    path('policies/terms/', views.terms_of_service, name='terms_of_service'),
    path('api/pincode/', views.check_pincode_view, name='check_pincode'),
]
