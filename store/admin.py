from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Coupon, Order, OrderItem, Review, Wishlist
from django.utils.html import format_html
from .utils import generate_admin_whatsapp_url

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}



class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ['size', 'stock']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4  # 4 additional image slots (Total 5 with primary image)
    fields = ['image', 'caption']
    verbose_name = 'Additional Angle / Photo'
    verbose_name_plural = 'Additional Gallery Photos (Upload 4 to 5 Angles Here)'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created']
    list_filter = ['available', 'category', 'created']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [ProductVariantInline, ProductImageInline]
    
    fieldsets = (
        ('1. Core Details', {
            'fields': ('name', 'category', 'price', 'image')
        }),
        ('2. Product Description & Story', {
            'fields': ('description',),
            'description': 'Enter the artwork details, fabric notes, and fit description here. This will show on both the product listing and detail pages.'
        }),
        ('3. Inventory & Visibility', {
            'fields': ('stock', 'available')
        }),
        ('4. Optional Technical Specs (Pre-filled defaults)', {
            'classes': ('collapse',),
            'fields': ('slug', 'fit_type', 'gsm', 'print_type')
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'caption', 'image_url', 'created']
    list_filter = ['created']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'active']
    list_filter = ['active']
    search_fields = ['code']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'paid', 'payment_method', 'status', 'awb_code', 'whatsapp_dispatch_link', 'created']
    list_filter = ['paid', 'status', 'created', 'payment_method']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'awb_code', 'id']
    readonly_fields = ['awb_code', 'whatsapp_dispatch_link']
    inlines = [OrderItemInline]

    def whatsapp_dispatch_link(self, obj):
        url = generate_admin_whatsapp_url(obj)
        return format_html('<a href="{}" target="_blank" style="padding: 4px 8px; background: #25D366; color: white; border-radius: 4px; font-weight: bold; text-decoration: none;">💬 WhatsApp Alert</a>', url)
    whatsapp_dispatch_link.short_description = 'WhatsApp Customer'



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created']
    list_filter = ['rating', 'created']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created']
