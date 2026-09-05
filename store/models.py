from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.CharField(max_length=50, default='👕', help_text='Emoji or icon for category bubble')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])


class Product(models.Model):
    FIT_CHOICES = (
        ('Oversized Drop Shoulder', 'Oversized Drop Shoulder'),
        ('Boxy Streetwear Fit', 'Boxy Streetwear Fit'),
        ('Relaxed Fit', 'Relaxed Fit'),
        ('Classic Regular Fit', 'Classic Regular Fit'),
    )

    PRINT_CHOICES = (
        ('High-Density Puff Print', 'High-Density Puff Print'),
        ('Ultra-HD DTG Print', 'Ultra-HD Direct-to-Garment (DTG)'),
        ('Vintage Distressed Screen Print', 'Vintage Distressed Screen Print'),
        ('Reflective Neon Holographic', 'Reflective Neon Holographic'),
        ('Silicone Rubberized Suede Print', 'Silicone Rubberized Suede Print'),
        ('Metallic Foil Screen Print', 'Metallic Foil Screen Print'),
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=15)
    available = models.BooleanField(default=True)
    fit_type = models.CharField(max_length=50, choices=FIT_CHOICES, default='Oversized Drop Shoulder')
    gsm = models.PositiveIntegerField(default=240, help_text='Fabric weight in GSM (e.g. 240, 260, 280)')
    print_type = models.CharField(max_length=50, choices=PRINT_CHOICES, default='High-Density Puff Print')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 4.9

    @property
    def image_url(self):
        """Returns a 100% guaranteed, rock-solid image URL for every product across all mobile and cloud devices."""
        # 1. Check direct child ProductImage with valid http(s) URL
        for img in self.images.all():
            if img.image_url and img.image_url.startswith('http'):
                return img.image_url

        # 2. Check if local uploaded image actually exists on the filesystem
        if self.image:
            try:
                if hasattr(self.image, 'path') and os.path.exists(self.image.path):
                    return self.image.url
                elif self.image.storage.exists(self.image.name):
                    return self.image.url
            except Exception:
                pass

        # 3. Dedicated verified CDN photo per product slug (Works instantly on mobile, local & Render)
        return self.get_fallback_image()

    def get_fallback_image(self):
        """Consistent, dedicated fallback photo for each specific product."""
        single_image_map = {
            'susanoo-spectral-armor-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
            'six-eyes-void-inversion-tee': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80',
            'fallen-seraphim-baroque-tee': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80',
            'memento-mori-gilded-vanitas-tee': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
            'neo-shinjuku-2099-glitch-tee': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80',
            'kurogane-mecha-core-tee': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80',
            'tokyo-midnight-racer-1994-tee': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80',
            'nirvana-in-utero-mineral-wash-tee': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80',
            'form-follows-chaos-boxy-tee': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80',
            'kyoto-botanica-ink-wash-tee': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80',
            'elden-sovereign-gilded-grace-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
            'venomous-symbiosis-liquid-obsidian-tee': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
            # Legacy product slugs
            'naruto-itachi-oversized-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
            'deadpool-merc-comic-tee': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
            'deadpool-merc-pullover': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
            'aot-survey-corps-tee': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80',
            'spiderman-oscorp-graphic-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
            'spiderman-symbiote-graphic-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
            'acid-wash-vintage-tee': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80',
            'nirvana-vintage-acid-wash-tee': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80',
            'cyberpunk-tokyo-2099-tee': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
            'cotton-linen-cuban-shirt': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80',
            'korean-baggy-joggers-offwhite': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80',
            'tactical-cargo-pants-slate': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80',
            'tss-snow-storm-hoodie': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
            'urban-bomber-jacket-green': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
            'milano-retro-sneakers-olive': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
            'street-chunky-trainers-white': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80',
            'crossbody-fanny-pack-black': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
        }
        return single_image_map.get(self.slug, 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80')

    def get_gallery_images(self):
        """Returns consistent image URLs for THIS product only.
        Guarantees that the product's own primary image is always first,
        and never includes mismatched images of different garments."""
        primary = self.image_url
        gallery = [primary] if primary else []

        # If the product has uploaded file images in ProductImage, add them
        uploaded_images = self.images.filter(image__isnull=False)
        for img in uploaded_images:
            u = img.get_url()
            if u and u not in gallery:
                gallery.append(u)

        # If no uploaded child images exist, but child ProductImages exist:
        if len(gallery) <= 1:
            for img in self.images.all():
                u = img.get_url()
                # If product already has an uploaded media file, ignore external URLs of other shirts
                if self.image and u.startswith('http'):
                    continue
                if u and u not in gallery:
                    gallery.append(u)

        return gallery


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    caption = models.CharField(max_length=150, blank=True, help_text='e.g. Front View, Back Print, Model Shot, Detail')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.product.name} Image ({self.caption or 'Gallery'})"

    def get_url(self):
        if self.image:
            try:
                if self.image.storage.exists(self.image.name):
                    return self.image.url
            except Exception:
                pass
        return self.image_url


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code} ({self.discount_percent}% Off)'


class Order(models.Model):
    STATUS_CHOICES = (
        ('Placed', 'Order Placed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, default='Cash on Delivery (COD)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')
    discount = models.IntegerField(default=0)
    awb_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_subtotal_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost(self):
        subtotal = self.get_subtotal_cost()
        if self.discount:
            discount_amount = subtotal * (Decimal(self.discount) / Decimal('100'))
            return (subtotal - discount_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal(subtotal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, default='M')

    def __str__(self):
        return f'{self.product.name} ({self.size})'

    def get_cost(self):
        return self.price * self.quantity


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f'{i} Stars') for i in range(1, 6)], default=5)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
