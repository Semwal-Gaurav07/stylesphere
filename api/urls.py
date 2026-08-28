from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'wishlist', views.WishlistViewSet, basename='wishlist')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', views.OrderCreateAPIView.as_view(), name='order_create_api'),
]
