#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Run migrations with automatic conflict resolution
python manage.py migrate --no-input || python manage.py migrate --fake-initial --no-input || python manage.py migrate --fake store --no-input

python manage.py seed_catalog || python seed_data.py || true
python download_images.py || true
