#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Applying database migrations..."
python manage.py migrate --no-input

echo "🌱 Seeding catalog data if needed..."
python manage.py seed_catalog || python seed_data.py || true

echo "🖼️ Ensuring fallback assets..."
python download_images.py || true

# Safe superuser creation: Only creates an admin if DJANGO_SUPERUSER_PASSWORD is provided in environment
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Ensuring superuser account..."
    python manage.py shell -c "
import os
from django.contrib.auth.models import User
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@stylesphere.in')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser \"{username}\" created.')
else:
    print(f'Superuser \"{username}\" already exists.')
"
fi

echo "✅ Build completed successfully!"
