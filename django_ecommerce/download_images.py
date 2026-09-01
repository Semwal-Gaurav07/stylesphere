import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Product
from django.core.files import File

tshirt_images = {
    'naruto-itachi-oversized-tee': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800',
    'cyberpunk-tokyo-2099-tee': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800',
    'aot-survey-corps-tee': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800',
    'spiderman-symbiote-graphic-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800',
    'nirvana-vintage-acid-wash-tee': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800',
    'jujutsu-kaisen-gojo-domain-tee': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800',
    'kanji-glitch-minimalist-tee': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800',
    'elden-ring-erdtree-graphic-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800',
    'deadpool-merc-comic-tee': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800',
    'retro-synthwave-80s-tee': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800',
    'minimalist-botanical-line-tee': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800',
    'death-note-ryuk-oversized-tee': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800',
}

headers = {'User-Agent': 'Mozilla/5.0'}

for slug, url in tshirt_images.items():
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

print("All printed t-shirt photos downloaded successfully!")
