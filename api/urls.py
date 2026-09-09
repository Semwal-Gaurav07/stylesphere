from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'wishlist', views.WishlistViewSet, basename='wishlist')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    
    # JWT Authentication Endpoints (For Mobile / React Frontend)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Order Management Endpoints
    path('orders/', views.OrderListCreateAPIView.as_view(), name='order_list_create_api'),
    path('orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='order_detail_api'),
    path('orders/<int:pk>/cancel/', views.OrderCancelAPIView.as_view(), name='order_cancel_api'),
    path('orders/track/<str:tracking_number>/', views.OrderTrackingAPIView.as_view(), name='order_tracking_api'),
]
