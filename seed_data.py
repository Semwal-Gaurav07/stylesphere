import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product

def seed():
    print("Seeding sample data...")

    cat_electronics, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
    cat_apparel, _ = Category.objects.get_or_create(name='Apparel', slug='apparel')
    cat_home, _ = Category.objects.get_or_create(name='Home & Living', slug='home-living')

    products_data = [
        {
            'category': cat_electronics,
            'name': 'Wireless Noise-Canceling Headphones',
            'slug': 'wireless-headphones',
            'description': 'High-fidelity audio with active noise cancellation and 30-hour battery life.',
            'price': 199.99,
            'available': True,
        },
        {
            'category': cat_electronics,
            'name': 'Smart Fitness Watch',
            'slug': 'smart-fitness-watch',
            'description': 'Track heart rate, workouts, sleep quality, and daily activity with GPS.',
            'price': 149.50,
            'available': True,
        },
        {
            'category': cat_apparel,
            'name': 'Classic Cotton Hoodie',
            'slug': 'classic-cotton-hoodie',
            'description': 'Ultra-soft fleece hoodie designed for everyday comfort and warmth.',
            'price': 49.99,
            'available': True,
        },
        {
            'category': cat_apparel,
            'name': 'Leather Minimalist Wallet',
            'slug': 'leather-wallet',
            'description': 'Genuine leather bi-fold wallet with RFID blocking technology.',
            'price': 29.95,
            'available': True,
        },
        {
            'category': cat_home,
            'name': 'Ceramic Pour-Over Coffee Maker',
            'slug': 'ceramic-coffee-maker',
            'description': 'Handcrafted ceramic coffee dripper for rich, smooth manual brew coffee.',
            'price': 34.00,
            'available': True,
        },
        {
            'category': cat_home,
            'name': 'Ergonomic Desk Lamp',
            'slug': 'ergonomic-desk-lamp',
            'description': 'LED desk lamp with adjustable brightness, color modes, and USB charging port.',
            'price': 59.90,
            'available': True,
        },
    ]

    for p in products_data:
        Product.objects.get_or_create(
            category=p['category'],
            name=p['name'],
            slug=p['slug'],
            defaults={
                'description': p['description'],
                'price': p['price'],
                'available': p['available']
            }
        )

    print("Seeding complete successfully!")

if __name__ == '__main__':
    seed()
