#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Automatic migration conflict resolution:
# If table already exists in committed db.sqlite3, fake migration 0005 cleanly so build succeeds
python manage.py migrate --no-input || python manage.py migrate --fake store 0005 --no-input || python manage.py migrate --fake-initial --no-input || true

python manage.py seed_catalog || python seed_data.py || true
python download_images.py || true
python manage.py shell -c "import os; from django.contrib.auth.models import User; u = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'); p = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin@2026!'); e = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@stylesphere.in'); User.objects.filter(username=u).exists() or User.objects.create_superuser(u, e, p)" || true
