from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category

class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Product.objects.filter(available=True).order_by('-updated')

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.all().order_by('name')

    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return [
            'store:product_list',
            'store:shipping_policy',
            'store:returns_policy',
            'store:privacy_policy',
            'store:terms_of_service',
            'store:provenance_vault',
            'store:midnight_vault',
        ]

    def location(self, item):
        return reverse(item)