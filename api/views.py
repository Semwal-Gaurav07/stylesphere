from rest_framework import viewsets, generics, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from store.models import Category, Product, Order, Review, Wishlist
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    ReviewSerializer,
    WishlistSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True).select_related('category').prefetch_related('images', 'variants', 'reviews')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'print_type', 'fit_type']
    ordering_fields = ['price', 'created']

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all().select_related('user', 'product')
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product', 'product__category')

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.filter(id=product_id, available=True).first()
        if not product:
            return Response({'error': 'Product not found or unavailable.'}, status=status.HTTP_404_NOT_FOUND)
        
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        serializer = self.get_serializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Backward compatibility alias
OrderCreateAPIView = OrderListCreateAPIView

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

class OrderTrackingAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, tracking_number):
        clean_num = str(tracking_number).strip()
        order = Order.objects.filter(tracking_number__iexact=clean_num).first() or \
                Order.objects.filter(awb_code__iexact=clean_num).first()
        
        if not order and clean_num.isdigit():
            order = Order.objects.filter(id=int(clean_num)).first()

        if not order:
            return Response({'error': 'No shipment found for this tracking number.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'order_id': order.id,
            'tracking_number': order.tracking_number,
            'awb_code': order.awb_code,
            'status': order.status,
            'created': order.created,
            'city': order.city,
            'payment_method': order.payment_method,
            'paid': order.paid,
            'items_count': order.items.count()
        })


class OrderCancelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        if order.status in ['Shipped', 'Delivered']:
            return Response({'error': f'Order cannot be cancelled because it is already {order.status.lower()}.'}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == 'Cancelled':
            return Response({'message': 'Order is already cancelled.'}, status=status.HTTP_200_OK)

        from django.db import transaction
        from django.db.models import F

        with transaction.atomic():
            for item in order.items.all():
                variant = item.product.variants.filter(size=item.size).first()
                if variant:
                    variant.stock = F('stock') + item.quantity
                    variant.save()
                Product.objects.filter(id=item.product.id).update(stock=F('stock') + item.quantity)
                Product.objects.filter(id=item.product.id, available=False).update(available=True)
            order.status = 'Cancelled'
            order.save()

        return Response({'message': f'Order #{order.id} cancelled successfully and inventory returned.', 'status': 'Cancelled'})
