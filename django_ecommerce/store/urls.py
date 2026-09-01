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
]
