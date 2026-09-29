from django.contrib.sitemaps.views import sitemap
from store.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /cart/",
        "Disallow: /orders/",
        "Disallow: /accounts/profile/",
        "Allow: /",
        "",
        "Sitemap: https://stylesphere-store.onrender.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

from django.http import HttpResponse, JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "healthy", "database": "connected"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "degraded", "error": str(e)}, status=500)

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('healthz', health_check, name='health_check'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('health/', health_check, name='health_check_slash'),
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('api/', include('api.urls', namespace='api')),
]

# Serve static/media
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
