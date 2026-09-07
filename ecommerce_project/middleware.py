"""
Project custom middleware.
"""

class CSRFOriginFixMiddleware:
    """
    Fixes 'Origin checking failed - null does not match any trusted origins'
    when users submit forms from mobile in-app browsers (WhatsApp, Instagram, Telegram WebViews),
    cross-origin privacy shields, or reverse-proxy HTTPS conversions on Render.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.META.get('HTTP_ORIGIN')
        if origin == 'null' or not origin:
            host = request.get_host()
            is_ssl = request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https'
            scheme = 'https' if is_ssl else 'http'
            request.META['HTTP_ORIGIN'] = f"{scheme}://{host}"
        return self.get_response(request)

class SecurityHeaderMiddleware:
    """
    Adds standard security headers to outgoing HTTP responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
