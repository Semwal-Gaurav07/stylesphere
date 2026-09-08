"""
Project custom middleware.
"""

class CSRFOriginFixMiddleware:
    """
    Handles instances where legitimate mobile in-app browsers (WhatsApp, Instagram, Telegram WebViews)
    send 'Origin: null' or omit the Origin header for same-site POST requests.
    Validates against the request's own Host and Referer to prevent blanket bypass.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.META.get('HTTP_ORIGIN')
        if origin == 'null' or not origin:
            referer = request.META.get('HTTP_REFERER')
            host = request.get_host()
            # Only synthesize Origin if the request demonstrably originated from our own host
            if referer and host in referer:
                is_ssl = request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https'
                scheme = 'https' if is_ssl else 'http'
                request.META['HTTP_ORIGIN'] = f"{scheme}://{host}"
        return self.get_response(request)

class SecurityHeaderMiddleware:
    """
    Adds essential modern HTTP security headers to outgoing responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=*, usb=()'
        return response
