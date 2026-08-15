import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Product
from django.core.files import File

# High-resolution Unsplash images for each streetwear product
sample_images = {
    # T-Shirts
    'naruto-itachi-oversized-tee': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600',
    'spiderman-oscorp-graphic-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600',
    'aot-survey-corps-tee': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=600',
    'acid-wash-vintage-tee': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=600',

    # Hoodies & Jackets
    'tss-snow-storm-hoodie': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600',
    'deadpool-merc-pullover': 'https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=600',
    'urban-bomber-jacket-green': 'https://images.unsplash.com/photo-1544441893-675973e31985?w=600',

    # Joggers & Cargoes
    'korean-baggy-joggers-offwhite': 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=600',
    'tactical-cargo-pants-slate': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600',

    # Sneakers
    'milano-retro-sneakers-olive': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600',
    'street-chunky-trainers-white': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600',

    # Shirts
    'cotton-linen-cuban-shirt': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600',

    # Accessories
    'crossbody-fanny-pack-black': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600',
}

headers = {'User-Agent': 'Mozilla/5.0'}

for slug, url in sample_images.items():
    try:
        product = Product.objects.get(slug=slug)
        req = urllib.request.Request(url, headers=headers)
        temp_file, _ = urllib.request.urlretrieve(url)
        with open(temp_file, 'rb') as f:
            product.image.save(f'{slug}.jpg', File(f), save=True)
        print(f"Downloaded image for: {product.name}")
    except Product.DoesNotExist:
        pass
    except Exception as e:
        print(f"Failed {slug}: {e}")

print("All streetwear product samples have been downloaded and attached successfully!")