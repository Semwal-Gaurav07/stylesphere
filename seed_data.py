import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product, Coupon

def seed():
    print("Seeding Style Sphere catalog & coupons...")

    # Coupons
    Coupon.objects.update_or_create(code='FIRST10', defaults={'discount_percent': 10, 'active': True})
    Coupon.objects.update_or_create(code='SAVE20', defaults={'discount_percent': 20, 'active': True})
    Coupon.objects.update_or_create(code='STAY5', defaults={'discount_percent': 5, 'active': True})

    # Categories
    cat_sneakers, _ = Category.objects.get_or_create(name='Sneakers & Kicks', slug='sneakers-kicks')
    cat_sunglasses, _ = Category.objects.get_or_create(name='Polarized Sunglasses', slug='polarized-sunglasses')
    cat_tshirts, _ = Category.objects.get_or_create(name='Oversized T-Shirts', slug='oversized-t-shirts')
    cat_hoodies, _ = Category.objects.get_or_create(name='Hoodies & Jackets', slug='hoodies-jackets')
    cat_bottoms, _ = Category.objects.get_or_create(name='Joggers & Cargoes', slug='joggers-cargoes')
    cat_accessories, _ = Category.objects.get_or_create(name='Accessories & Bags', slug='accessories-bags')

    products = [
        {
            'category': cat_sneakers,
            'name': 'Cyberpunk High-Top Runner',
            'slug': 'cyberpunk-high-top-runner',
            'description': 'Nitrogen-infused kinetic sole with reflective cyber-mesh and aerodynamic heel lock.',
            'price': 1899.00,
            'stock': 12,
            'available': True,
        },
        {
            'category': cat_sunglasses,
            'name': 'Matrix Hexagon Polarized Shades',
            'slug': 'matrix-hexagon-polarized-shades',
            'description': 'Lightweight titanium frame with dark-tint polarized lenses protecting 100% UVA/UVB rays.',
            'price': 899.00,
            'stock': 15,
            'available': True,
        },
        {
            'category': cat_tshirts,
            'name': 'Naruto: Itachi Uchiha Oversized Tee',
            'slug': 'naruto-itachi-oversized-tee',
            'description': '240 GSM heavy-gauge French Terry cotton oversized t-shirt with high-definition Itachi back print.',
            'price': 899.00,
            'stock': 12,
            'available': True,
        },
        {
            'category': cat_tshirts,
            'name': 'Spider-Man: Oscorp Suit Graphic Tee',
            'slug': 'spiderman-oscorp-graphic-tee',
            'description': 'Official Marvel Studios licensed oversized drop-shoulder graphic t-shirt.',
            'price': 849.00,
            'stock': 15,
            'available': True,
        },
        {
            'category': cat_hoodies,
            'name': 'TSS Originals: Snow Storm Heavy Hoodie',
            'slug': 'tss-snow-storm-hoodie',
            'description': '400 GSM heavyweight fleece winter pullover with double-layered hood and kangaroo pocket.',
            'price': 1499.00,
            'stock': 8,
            'available': True,
        },
        {
            'category': cat_bottoms,
            'name': 'Korean Baggy Fit Joggers: Off-White',
            'slug': 'korean-baggy-joggers-offwhite',
            'description': 'Relaxed baggy silhouette with elasticated drawstring waistband and ankle cuffs.',
            'price': 1199.00,
            'stock': 14,
            'available': True,
        },
        {
            'category': cat_accessories,
            'name': 'Crossbody Tactical Fanny Pack: Black',
            'slug': 'crossbody-fanny-pack-black',
            'description': 'Waterproof ripstop fabric with adjustable buckle strap, key clip, and quick-access zippers.',
            'price': 699.00,
            'stock': 16,
            'available': True,
        },
    ]

    for p in products:
        Product.objects.update_or_create(
            slug=p['slug'],
            defaults={
                'category': p['category'],
                'name': p['name'],
                'description': p['description'],
                'price': p['price'],
                'stock': p['stock'],
                'available': p['available']
            }
        )

    print("Seed complete with coupons and product catalog!")

if __name__ == '__main__':
    seed()
