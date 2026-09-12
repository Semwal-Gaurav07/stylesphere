from rest_framework import serializers
from store.models import Category, Product, ProductImage, Order, OrderItem, Review, Wishlist

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'caption', 'url']

    def get_url(self, obj):
        return obj.get_url()


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'username', 'rating', 'comment', 'created']
        read_only_fields = ['user']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    average_rating = serializers.ReadOnlyField(source='get_average_rating')
    image_url = serializers.ReadOnlyField()
    gallery_images = serializers.ReadOnlyField(source='get_gallery_images')
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 'slug', 'image_url',
            'gallery_images', 'images', 'description', 'price', 'stock',
            'available', 'fit_type', 'gsm', 'print_type', 'average_rating',
            'reviews', 'created', 'updated'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'size']


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
    size = serializers.CharField(default='M', max_length=10)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_items = OrderItemCreateSerializer(many=True, write_only=True, required=False)
    total_cost = serializers.ReadOnlyField(source='get_total_cost')

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'address',
            'postal_code', 'city', 'paid', 'payment_method', 'status',
            'discount', 'awb_code', 'tracking_number', 'total_cost', 'items', 'order_items', 'created'
        ]
        read_only_fields = ['user', 'paid', 'status', 'awb_code', 'tracking_number', 'total_cost', 'created']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items', [])
        from django.db import transaction
        from django.db.models import F

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item in items_data:
                product = Product.objects.filter(id=item['product_id'], available=True).first()
                if not product:
                    raise serializers.ValidationError(f"Product ID {item['product_id']} not found or unavailable.")
                qty = item['quantity']
                size = item.get('size', 'M')

                # Check and atomic deduct stock
                size_variant = product.variants.filter(size=size).first()
                if size_variant:
                    rows = product.variants.filter(id=size_variant.id, stock__gte=qty).update(stock=F('stock') - qty)
                    Product.objects.filter(id=product.id).update(stock=F('stock') - qty)
                else:
                    rows = Product.objects.filter(id=product.id, stock__gte=qty).update(stock=F('stock') - qty)

                if not rows:
                    raise serializers.ValidationError(f"Insufficient stock for {product.name} (Size {size}).")

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=qty,
                    size=size
                )
        return order
class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id', 'created']
        read_only_fields = ['user']
