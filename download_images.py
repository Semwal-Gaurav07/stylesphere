import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Product
from django.core.files import File

sample_images = {
    'wireless-headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
    'smart-fitness-watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500',
    'classic-cotton-hoodie': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500',
    'leather-wallet': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=500',
    'ceramic-coffee-maker': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500',
    'ergonomic-desk-lamp': 'https://images.unsplash.com/photo-1534073828943-f801091bb18c?w=500',
}

for slug, url in sample_images.items():
    try:
        product = Product.objects.get(slug=slug)
        temp_file, _ = urllib.request.urlretrieve(url)
        with open(temp_file, 'rb') as f:
            product.image.save(f'{slug}.jpg', File(f), save=True)
        print(f"Downloaded image for: {product.name}")
    except Product.DoesNotExist:
        pass

print("Finished downloading sample images!")
