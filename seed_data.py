import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product, ProductImage, Coupon

def seed():
    print("Seeding Style Sphere Atelier — Exclusive Luxury Streetwear Collection...")

    # Create 6 Elevated Luxury Streetwear Categories
    cat_anime, _ = Category.objects.get_or_create(
        slug='anime-graphic-tees',
        defaults={'name': 'Anime & Manga Atelier', 'icon': '⚔️'}
    )
    cat_anime.name = 'Anime & Manga Atelier'
    cat_anime.icon = '⚔️'
    cat_anime.save()

    cat_renaissance, _ = Category.objects.get_or_create(
        slug='dark-renaissance-tees',
        defaults={'name': 'Dark Renaissance & Baroque', 'icon': '🏛️'}
    )
    cat_renaissance.name = 'Dark Renaissance & Baroque'
    cat_renaissance.icon = '🏛️'
    cat_renaissance.save()

    cat_cyberpunk, _ = Category.objects.get_or_create(
        slug='cyberpunk-graphic-tees',
        defaults={'name': 'Cyberpunk & Neo-Tokyo', 'icon': '🤖'}
    )
    cat_cyberpunk.name = 'Cyberpunk & Neo-Tokyo'
    cat_cyberpunk.icon = '🤖'
    cat_cyberpunk.save()

    cat_vintage, _ = Category.objects.get_or_create(
        slug='vintage-pop-culture-tees',
        defaults={'name': 'Vintage Mineral & Acid Wash', 'icon': '⚡'}
    )
    cat_vintage.name = 'Vintage Mineral & Acid Wash'
    cat_vintage.icon = '⚡'
    cat_vintage.save()

    cat_minimalist, _ = Category.objects.get_or_create(
        slug='minimalist-typography-tees',
        defaults={'name': 'Brutalist & Modern Typography', 'icon': '✒️'}
    )
    cat_minimalist.name = 'Brutalist & Modern Typography'
    cat_minimalist.icon = '✒️'
    cat_minimalist.save()

    cat_fandom, _ = Category.objects.get_or_create(
        slug='gaming-fandom-tees',
        defaults={'name': 'Dark Fantasy & Fandom Atelier', 'icon': '🎮'}
    )
    cat_fandom.name = 'Dark Fantasy & Fandom Atelier'
    cat_fandom.icon = '🎮'
    cat_fandom.save()

    # Seed Luxury Promo Coupons
    Coupon.objects.get_or_create(code='FIRST10', defaults={'discount_percent': 10, 'active': True})
    Coupon.objects.get_or_create(code='TEES20', defaults={'discount_percent': 20, 'active': True})
    Coupon.objects.get_or_create(code='STAY5', defaults={'discount_percent': 5, 'active': True})

    # 12 Curated Luxury Streetwear Flagship Pieces (Each with a dedicated, consistent image)
    luxury_products = [
        # 1. Anime & Manga Atelier
        {
            'category': cat_anime,
            'name': "Susano'o Spectral Armor // High-Density 3D Puff Tee",
            'slug': 'susanoo-spectral-armor-tee',
            'description': 'Crafted from heavyweight 260 GSM French Terry cotton in an architectural drop-shoulder cut. Features an understated chest calligraphy seal on the front, anchored by a monolithic, ultra-tactile 3D puff print of the ethereal samurai avatar on the back with liquid violet flames and pre-shrunk carbon wash.',
            'price': 1199.00,
            'stock': 14,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 260,
            'print_type': 'High-Density Puff Print',
            'image_url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
        },
        {
            'category': cat_anime,
            'name': 'Six Eyes: Void Inversion // High-Density Suede Boxy Tee',
            'slug': 'six-eyes-void-inversion-tee',
            'description': 'Tailored in 280 GSM combed compact cotton for supreme structure and drape. Showcases minimalist Japanese vertical typography on the chest pocket and a multi-layered spatial distortion backprint finished with rubberized suede touch ink and anti-pilling bio-wash.',
            'price': 1299.00,
            'stock': 18,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 280,
            'print_type': 'Silicone Rubberized Suede Print',
            'image_url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80',
        },

        # 2. Dark Renaissance & Baroque
        {
            'category': cat_renaissance,
            'name': 'Fallen Seraphim // Baroque Marble & Liquid Chrome Tee',
            'slug': 'fallen-seraphim-baroque-tee',
            'description': 'Chiaroscuro fine art meets high-street subversion. 260 GSM bio-washed French Terry featuring micro-embossed antique Roman numeral insignia on the chest and an expansive photorealistic backprint of classical angelic marble dissolving into liquid mercury chrome foil.',
            'price': 1349.00,
            'stock': 12,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 260,
            'print_type': 'Metallic Foil Screen Print',
            'image_url': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80',
        },
        {
            'category': cat_renaissance,
            'name': 'Memento Mori // Gilded Vanitas Botanical Heavyweight Tee',
            'slug': 'memento-mori-gilded-vanitas-tee',
            'description': 'Forged in 250 GSM aged bone-white heavyweight cotton. Detailed with a clean botanical laurel crest over the left chest and a museum-grade archival copperplate etching of skull and withered flora on the back highlighted with antique gold leaf pigments.',
            'price': 1099.00,
            'stock': 15,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 250,
            'print_type': 'Metallic Foil Screen Print',
            'image_url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
        },

        # 3. Cyberpunk & Neo-Tokyo
        {
            'category': cat_cyberpunk,
            'name': 'Neo-Shinjuku 2099 // Cyber-Geisha Glitch Matrix Tee',
            'slug': 'neo-shinjuku-2099-glitch-tee',
            'description': 'Constructed from 260 GSM carbon-washed jet cotton with high-stretch ribbed collar. Features technical coordinate barcodes on the front hem and a multi-dimensional cybernetic glitch geisha back artwork with UV-reactive luminescence and reflective holographic inks.',
            'price': 1249.00,
            'stock': 16,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 260,
            'print_type': 'Reflective Neon Holographic',
            'image_url': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80',
        },
        {
            'category': cat_cyberpunk,
            'name': 'Kurogane Mecha Core // Tactical Structural Blueprint Tee',
            'slug': 'kurogane-mecha-core-tee',
            'description': 'Engineered on 270 GSM double-combed iron slate cotton with reinforced shoulder tapes. Minimalist warning glyphs on the front chest harmonize with a comprehensive exploded-view mechanized chassis blueprint across the back in raised rubberized ink.',
            'price': 1149.00,
            'stock': 19,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 270,
            'print_type': 'Silicone Rubberized Suede Print',
            'image_url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80',
        },

        # 4. Vintage Mineral & Acid Wash
        {
            'category': cat_vintage,
            'name': 'Tokyo Midnight Racer 1994 // Acid Wash Relic Tee',
            'slug': 'tokyo-midnight-racer-1994-tee',
            'description': 'Individual manual acid-wash treatment on 250 GSM heavy cotton creating a unique smoke-charcoal patina on every piece. Front features an authentic retro tachometer emblem, while the back displays a distressed halftone montage of iconic 90s Wangan midnight highway racers.',
            'price': 1099.00,
            'stock': 20,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 250,
            'print_type': 'Vintage Distressed Screen Print',
            'image_url': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80',
        },
        {
            'category': cat_vintage,
            'name': 'Nirvana In Utero // Aged Mineral Washed Heavyweight Tee',
            'slug': 'nirvana-in-utero-mineral-wash-tee',
            'description': 'A tribute to grunge royalty. 240 GSM pre-shrunk mineral washed vintage black cotton with hand-distressed neck ribbing. Front features the legendary transparent anatomical angel, backed by distressed archival 1993 tour dates rendered in cracked plastisol screen print.',
            'price': 999.00,
            'stock': 22,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 240,
            'print_type': 'Vintage Distressed Screen Print',
            'image_url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80',
        },

        # 5. Brutalist & Modern Typography
        {
            'category': cat_minimalist,
            'name': 'Form Follows Chaos // Architectural Monogram Boxy Tee',
            'slug': 'form-follows-chaos-boxy-tee',
            'description': 'Strict architectural minimalism. 260 GSM combed ring-spun cotton in chalk white. Features a blind tonal debossed StyleSphere atelier stamp on the front chest and a razor-sharp Swiss typographic manifesto exploring structural balance and asymmetric grids on the back.',
            'price': 899.00,
            'stock': 25,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 260,
            'print_type': 'Ultra-HD DTG Print',
            'image_url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80',
        },
        {
            'category': cat_minimalist,
            'name': 'Kyoto Botanica // Ethereal Sumi-e Ink Wash Heavyweight Tee',
            'slug': 'kyoto-botanica-ink-wash-tee',
            'description': 'Traditional Japanese sumi-e wash reimagined for modern luxury streetwear. 250 GSM organic unbleached cream cotton. Features an authentic crimson hanko seal stamp embroidered on the front, complemented by an expressive weeping bamboo and moon watercolor splash across the back.',
            'price': 949.00,
            'stock': 17,
            'fit_type': 'Relaxed Fit',
            'gsm': 250,
            'print_type': 'Ultra-HD DTG Print',
            'image_url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80',
        },

        # 6. Dark Fantasy & Fandom Atelier
        {
            'category': cat_fandom,
            'name': 'Elden Sovereign // Gilded Grace & Erdtree Metallic Foil Tee',
            'slug': 'elden-sovereign-gilded-grace-tee',
            'description': 'Royal dark fantasy executed in couture streetwear proportions. 260 GSM French Terry in pitch-black finish. Minimalist golden rune emblem on the breast is contrasted by an arresting golden metallic foil backprint depicting the burning Erdtree in radiant filigree detail.',
            'price': 1299.00,
            'stock': 13,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 260,
            'print_type': 'Metallic Foil Screen Print',
            'image_url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80',
        },
        {
            'category': cat_fandom,
            'name': 'Venomous Symbiosis // Liquid Obsidian 3D Puff Streetwear Tee',
            'slug': 'venomous-symbiosis-liquid-obsidian-tee',
            'description': 'Visceral biomechanical streetwear. 270 GSM heavyweight French Terry in midnight noir. Subtle white spider fang mark on the chest with a ferocious, ultra-dimensional 3D puff and high-gloss wet-look backprint depicting symbiotic tendrils spreading across the shoulder blades.',
            'price': 1249.00,
            'stock': 15,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 270,
            'print_type': 'High-Density Puff Print',
            'image_url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80',
        },
    ]

    for p in luxury_products:
        prod, created = Product.objects.update_or_create(
            slug=p['slug'],
            defaults={
                'category': p['category'],
                'name': p['name'],
                'description': p['description'],
                'price': p['price'],
                'stock': p['stock'],
                'fit_type': p['fit_type'],
                'gsm': p['gsm'],
                'print_type': p['print_type'],
                'available': True
            }
        )
        
        # Clean up any legacy mismatched external URLs
        prod.images.filter(image_url__startswith='http').delete()
        
        # If product has no local media file uploaded, attach 1 single consistent image
        if not prod.image:
            ProductImage.objects.create(
                product=prod,
                image_url=p['image_url'],
                caption='Studio View'
            )

    print(f"Successfully seeded {len(luxury_products)} luxury streetwear pieces without mismatched images!")

if __name__ == '__main__':
    seed()
