import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product, Coupon

def seed():
    print("Seeding Style Sphere streetwear catalog...")

    # Coupons
    Coupon.objects.update_or_create(code='FIRST10', defaults={'discount_percent': 10, 'active': True})
    Coupon.objects.update_or_create(code='SAVE20', defaults={'discount_percent': 20, 'active': True})
    Coupon.objects.update_or_create(code='STAY5', defaults={'discount_percent': 5, 'active': True})

    # Categories
    cat_sneakers, _ = Category.objects.get_or_create(name='Sneakers & Footwear', slug='sneakers-footwear')
    cat_sunglasses, _ = Category.objects.get_or_create(name='Sunglasses & Optics', slug='sunglasses-optics')
    cat_tshirts, _ = Category.objects.get_or_create(name='Oversized T-Shirts', slug='oversized-t-shirts')
    cat_hoodies, _ = Category.objects.get_or_create(name='Hoodies & Jackets', slug='hoodies-jackets')
    cat_bottoms, _ = Category.objects.get_or_create(name='Joggers & Cargoes', slug='joggers-cargoes')
    cat_shirts, _ = Category.objects.get_or_create(name='Casual Shirts', slug='casual-shirts')
    cat_accessories, _ = Category.objects.get_or_create(name='Accessories & Bags', slug='accessories-bags')

    products = [
        # Sneakers & Sunglasses (Hero Category Items)
        {
            'category': cat_sneakers,
            'name': 'Cyberpunk High-Top Runner',
            'slug': 'cyberpunk-high-top-runner',
            'description': 'Nitrogen-infused kinetic sole with reflective cyber-mesh and aerodynamic heel lock.',
            'price': 1899.00,
            'stock': 8,
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
            'category': cat_sneakers,
            'name': 'Milano Retro Low-Top Sneakers: Olive',
            'slug': 'milano-retro-sneakers-olive',
            'description': 'Vegan leather upper with padded collar, breathable perforations, and vulcanized rubber grip sole.',
            'price': 1699.00,
            'stock': 5,
            'available': True,
        },
        {
            'category': cat_sneakers,
            'name': 'Street Chunky Platform Trainers: White',
            'slug': 'street-chunky-trainers-white',
            'description': 'Ultra-cushioned EVA midsole trainers designed for all-day streetwear comfort.',
            'price': 1799.00,
            'stock': 7,
            'available': True,
        },

        # Oversized T-Shirts
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
            'category': cat_tshirts,
            'name': 'Attack On Titan: Survey Corps Tee',
            'slug': 'aot-survey-corps-tee',
            'description': 'Super-oversized boxy fit tee with distressed green Wings of Freedom graphic.',
            'price': 899.00,
            'stock': 2,
            'available': True,
        },
        {
            'category': cat_tshirts,
            'name': 'Acid Wash Vintage Heavyweight Tee',
            'slug': 'acid-wash-vintage-tee',
            'description': '100% bio-washed vintage charcoal streetwear tee with relaxed ribbed neckline.',
            'price': 799.00,
            'stock': 20,
            'available': True,
        },

        # Hoodies & Jackets
        {
            'category': cat_hoodies,
            'name': 'TSS Originals: Snow Storm Heavy Hoodie',
            'slug': 'tss-snow-storm-hoodie',
            'description': '400 GSM heavyweight fleece winter pullover with double-layered hood and kangaroo pocket.',
            'price': 1999.00,
            'stock': 8,
            'available': True,
        },
        {
            'category': cat_hoodies,
            'name': 'Deadpool: Merc with a Mouth Pullover',
            'slug': 'deadpool-merc-pullover',
            'description': 'Vibrant red and black colorblock graphic hoodie with brushed inner warmth.',
            'price': 1799.00,
            'stock': 3,
            'available': True,
        },
        {
            'category': cat_hoodies,
            'name': 'Urban Bomber Jacket: Hunter Green',
            'slug': 'urban-bomber-jacket-green',
            'description': 'Water-resistant nylon shell bomber jacket with quilted orange lining and utility sleeve pocket.',
            'price': 2499.00,
            'stock': 6,
            'available': True,
        },

        # Joggers & Cargoes
        {
            'category': cat_bottoms,
            'name': 'Korean Baggy Fit Joggers: Off-White',
            'slug': 'korean-baggy-joggers-offwhite',
            'description': 'Relaxed baggy silhouette with elasticated drawstring waistband and ankle cuffs.',
            'price': 1299.00,
            'stock': 14,
            'available': True,
        },
        {
            'category': cat_bottoms,
            'name': '6-Pocket Tactical Cargo Pants: Slate',
            'slug': 'tactical-cargo-pants-slate',
            'description': 'Durable cotton-twill utility cargo trousers with reinforced knee panels and deep pockets.',
            'price': 1499.00,
            'stock': 9,
            'available': True,
        },

        # Casual Shirts
        {
            'category': cat_shirts,
            'name': 'Midnight Cotton Linen Cuban Shirt',
            'slug': 'cotton-linen-cuban-shirt',
            'description': 'Resort collar breathable cotton-linen blend shirt with relaxed drop-shoulder cut.',
            'price': 1199.00,
            'stock': 10,
            'available': True,
        },

        # Accessories
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

    print(f"Successfully seeded {len(products)} products and coupons (FIRST10, SAVE20, STAY5)!")

if __name__ == '__main__':
    seed()
