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


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.ReadOnlyField(source='get_total_cost')

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'address',
            'postal_code', 'city', 'paid', 'payment_method', 'status',
            'discount', 'awb_code', 'total_cost', 'items', 'created'
        ]


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id', 'created']
        read_only_fields = ['user']
