import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product, ProductImage, Coupon

def seed():
    print("Seeding Style Sphere - Exclusive Printed T-Shirts Studio...")

    # Protect existing orders: only seed if catalog is empty
    if Product.objects.count() >= 12:
        print("Catalog already seeded with 12 flagship printed t-shirts. Preserving customer orders and stock.")
        return

    # Create Printed T-Shirt Categories
    cat_anime, _ = Category.objects.get_or_create(
        name='Anime & Manga Graphic Tees',
        slug='anime-graphic-tees',
        defaults={'icon': '🔥'}
    )
    cat_streetwear, _ = Category.objects.get_or_create(
        name='Oversized & Acid Wash Tees',
        slug='oversized-streetwear-tees',
        defaults={'icon': '⚡'}
    )
    cat_cyberpunk, _ = Category.objects.get_or_create(
        name='Cyberpunk & Sci-Fi Graphic Tees',
        slug='cyberpunk-graphic-tees',
        defaults={'icon': '🤖'}
    )
    cat_vintage, _ = Category.objects.get_or_create(
        name='Vintage & Retro Pop Culture Tees',
        slug='vintage-pop-culture-tees',
        defaults={'icon': '📻'}
    )
    cat_minimalist, _ = Category.objects.get_or_create(
        name='Minimalist & Typography Art Tees',
        slug='minimalist-typography-tees',
        defaults={'icon': '✒️'}
    )
    cat_fandom, _ = Category.objects.get_or_create(
        name='Marvel, DC & Gaming Graphic Tees',
        slug='gaming-fandom-tees',
        defaults={'icon': '🎮'}
    )

    # Seed Coupons
    Coupon.objects.get_or_create(code='FIRST10', defaults={'discount_percent': 10, 'active': True})
    Coupon.objects.get_or_create(code='TEES20', defaults={'discount_percent': 20, 'active': True})
    Coupon.objects.get_or_create(code='STAY5', defaults={'discount_percent': 5, 'active': True})

    # Curated Printed T-Shirts (Each with 4 High-Res Images)
    tshirt_products = [
        {
            'category': cat_anime,
            'name': 'Naruto: Itachi Uchiha Mangekyo Graphic Tee',
            'slug': 'naruto-itachi-oversized-tee',
            'description': '240 GSM heavy French Terry cotton with high-definition Mangekyo Sharingan and crow silhouette back artwork. Features drop-shoulder oversized boxy silhouette and pre-shrunk bio-wash treatment.',
            'price': 899.00,
            'stock': 18,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 240,
            'print_type': 'Ultra-HD DTG Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Chest Logo'},
                {'url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Itachi Artwork'},
                {'url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80', 'caption': 'Streetwear On-Body Fit'},
                {'url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80', 'caption': 'Fabric & Ribbed Collar Macro'},
            ]
        },
        {
            'category': cat_cyberpunk,
            'name': 'Cyberpunk Tokyo 2099 Neon Oversized Tee',
            'slug': 'cyberpunk-tokyo-2099-tee',
            'description': 'Futuristic Japanese cyber-grid illustration with reflective UV-reactive neon accents. Engineered on 260 GSM combed cotton with high-stretch lycra ribbed crew neckline.',
            'price': 949.00,
            'stock': 14,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 260,
            'print_type': 'Reflective Neon Holographic',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Cyber Graphic'},
                {'url': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Kanji Grid'},
                {'url': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80', 'caption': 'Night City Aesthetic Model'},
                {'url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80', 'caption': 'Holographic Ink Texture Close-up'},
            ]
        },
        {
            'category': cat_anime,
            'name': 'Attack On Titan: Survey Corps Wings of Freedom Tee',
            'slug': 'aot-survey-corps-tee',
            'description': 'Super-oversized boxy fit tee with vintage distressed Wings of Freedom emblem on back. Bio-washed charcoal cotton for a lived-in vintage drape.',
            'price': 899.00,
            'stock': 8,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 240,
            'print_type': 'Vintage Distressed Screen Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Minimal Crest'},
                {'url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Wings of Freedom'},
                {'url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80', 'caption': 'Relaxed Drop-Shoulder Silhouette'},
                {'url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80', 'caption': 'Screen Print Weave Detail'},
            ]
        },
        {
            'category': cat_fandom,
            'name': 'Spider-Man: Symbiote Unleashed Graphic Tee',
            'slug': 'spiderman-symbiote-graphic-tee',
            'description': 'Official Marvel Studios inspired oversized graphic tee featuring 3D puff-printed symbiote tendrils and venomous comic graphics across front and back.',
            'price': 849.00,
            'stock': 20,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 240,
            'print_type': 'High-Density Puff Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Symbiote Emblem'},
                {'url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Graphic - Comic Cover Art'},
                {'url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80', 'caption': 'Street Styling On-Body Shot'},
                {'url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80', 'caption': '3D Puff Print Macro Close-up'},
            ]
        },
        {
            'category': cat_streetwear,
            'name': 'Acid Wash Vintage Mineral Heavyweight Tee',
            'slug': 'nirvana-vintage-acid-wash-tee',
            'description': '100% heavy mineral washed 240 GSM cotton tee with distressed graphic aesthetic, raw edge detailing, and ribbed thick crewneck.',
            'price': 799.00,
            'stock': 25,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 240,
            'print_type': 'Vintage Distressed Screen Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80', 'caption': 'Front Mineral Wash Look'},
                {'url': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Distressed Typography'},
                {'url': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80', 'caption': 'Skater Streetwear Model Pose'},
                {'url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80', 'caption': 'Heavy Mineral Wash Texture'},
            ]
        },
        {
            'category': cat_anime,
            'name': 'Jujutsu Kaisen: Gojo Satoru Domain Expansion Tee',
            'slug': 'jujutsu-kaisen-gojo-domain-tee',
            'description': 'High-density DTG illustration of Satoru Gojo invoking Unlimited Void. Deep black 260 GSM combed cotton with silky smooth hand feel.',
            'price': 949.00,
            'stock': 12,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 260,
            'print_type': 'Ultra-HD DTG Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Cyan Domain Sigil'},
                {'url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Gojo Satoru Art'},
                {'url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80', 'caption': 'Studio Model Drop Shoulder View'},
                {'url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80', 'caption': 'Color Saturation Ink Detail'},
            ]
        },
        {
            'category': cat_minimalist,
            'name': 'Aesthetic Kanji & Glitch Minimalist Art Tee',
            'slug': 'kanji-glitch-minimalist-tee',
            'description': 'Sleek monochromatic Japanese typography paired with subtle distortion graphic on left chest and back spine. Suede rubberized tactile feel.',
            'price': 749.00,
            'stock': 16,
            'fit_type': 'Relaxed Fit',
            'gsm': 240,
            'print_type': 'Silicone Rubberized Suede Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Minimal Kanji'},
                {'url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Spine - Glitch Typography'},
                {'url': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80', 'caption': 'Urban Neutral Outfit Shot'},
                {'url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80', 'caption': 'Tactile Rubber Ink Macro'},
            ]
        },
        {
            'category': cat_fandom,
            'name': 'Elden Ring: Shadow of the Erdtree Graphic Tee',
            'slug': 'elden-ring-erdtree-graphic-tee',
            'description': 'Gilded metallic foil accents combined with pitch-black screen print depicting the burning Erdtree. Heavyweight 250 GSM French Terry.',
            'price': 899.00,
            'stock': 9,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 250,
            'print_type': 'Metallic Foil Screen Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Erdtree Sigil'},
                {'url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Messmer Artwork'},
                {'url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80', 'caption': 'Drop-Shoulder Silhouette Model'},
                {'url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80', 'caption': 'Gold Metallic Foil Sheen'},
            ]
        },
        {
            'category': cat_fandom,
            'name': 'Deadpool: Merc with a Mouth Comic Graphic Tee',
            'slug': 'deadpool-merc-comic-tee',
            'description': 'High-octane comic colorblock print with vibrant crimson and obsidian ink. 240 GSM 100% super-combed cotton.',
            'price': 849.00,
            'stock': 15,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 240,
            'print_type': 'High-Density Puff Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Deadpool Mask'},
                {'url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Comic Action Panel'},
                {'url': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80', 'caption': 'Casual Street Style Fit'},
                {'url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80', 'caption': 'Durable Ribbed Collar Detail'},
            ]
        },
        {
            'category': cat_vintage,
            'name': 'Retro Synthwave 80s Sunset Oversized Tee',
            'slug': 'retro-synthwave-80s-tee',
            'description': 'Warm neon sunset gradient print with retro wireframe perspective grid and 80s arcade aesthetic on washed jet-black cotton.',
            'price': 799.00,
            'stock': 22,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 240,
            'print_type': 'Ultra-HD DTG Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - 80s Grid Sunset'},
                {'url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Outrun Typography'},
                {'url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80', 'caption': 'Dusk Street Wear Model'},
                {'url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80', 'caption': 'Gradient Color Fade Detail'},
            ]
        },
        {
            'category': cat_minimalist,
            'name': 'Minimalist Botanical Line Art Boxy Tee',
            'slug': 'minimalist-botanical-line-tee',
            'description': 'Elegant single-needle fine line illustration screen printed on 220 GSM eco-organic combed cotton with relaxed side vents.',
            'price': 699.00,
            'stock': 19,
            'fit_type': 'Boxy Streetwear Fit',
            'gsm': 220,
            'print_type': 'Vintage Distressed Screen Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Botanical Line Art'},
                {'url': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Clean Script'},
                {'url': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800&auto=format&fit=crop&q=80', 'caption': 'Minimal Clean Model Fit'},
                {'url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80', 'caption': 'Fine Cotton Weave Close-up'},
            ]
        },
        {
            'category': cat_anime,
            'name': 'Death Note: Ryuk Shinigami Oversized Graphic Tee',
            'slug': 'death-note-ryuk-oversized-tee',
            'description': 'High-contrast gothic Ryuk back print with crimson apple chest pocket motif. 260 GSM heavyweight French Terry with anti-pilling wash.',
            'price': 899.00,
            'stock': 11,
            'fit_type': 'Oversized Drop Shoulder',
            'gsm': 260,
            'print_type': 'High-Density Puff Print',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80', 'caption': 'Front View - Shinigami Apple Icon'},
                {'url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80', 'caption': 'Back Print - Ryuk Illustration'},
                {'url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80', 'caption': 'Gothic Streetwear Model View'},
                {'url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80', 'caption': 'High-Density Ink Density Macro'},
            ]
        }
    ]

    for p in tshirt_products:
        prod, _ = Product.objects.update_or_create(
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
        
        # Attach 4 ProductImage records
        for img_data in p.get('images', []):
            ProductImage.objects.create(
                product=prod,
                image_url=img_data['url'],
                caption=img_data['caption']
            )

    print(f"Successfully seeded {len(tshirt_products)} printed t-shirts (each with 4 gallery images) and 6 categories!")

if __name__ == '__main__':
    seed()
