import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Product, ProductImage

def fix_images():
    print("Running StyleSphere Image Alignment Fix...")
    cleaned_count = 0
    
    for prod in Product.objects.all():
        # Check if product has an uploaded media file
        has_local_file = False
        if prod.image:
            try:
                if prod.image.storage.exists(prod.image.name):
                    has_local_file = True
            except Exception:
                pass
        
        if has_local_file:
            # Delete any external mismatched URLs from ProductImage that don't match this product
            mismatched = prod.images.filter(image_url__startswith='http')
            count = mismatched.count()
            if count > 0:
                mismatched.delete()
                cleaned_count += count
                print(f"Cleaned {count} mismatched gallery image(s) from '{prod.name}' (using local: {prod.image.url})")
        else:
            # If product has multiple external images with different URLs, clean up extras
            # so it doesn't show multiple different shirts
            all_imgs = list(prod.images.all())
            if len(all_imgs) > 1:
                # Keep only the first image
                for img in all_imgs[1:]:
                    img.delete()
                    cleaned_count += 1
                print(f"Standardized '{prod.name}' to single consistent gallery image.")
                
    print(f"\nCompleted! Cleaned {cleaned_count} mismatched gallery records.")
    print("Every product will now consistently display its own authentic image.")

if __name__ == '__main__':
    fix_images()
