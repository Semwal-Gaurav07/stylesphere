class CSRFNullOriginFixMiddleware:
    """
    Fixes 'Origin checking failed - null does not match any trusted origins'
    when mobile users submit forms from in-app browsers (WhatsApp, Instagram, Telegram WebViews)
    or across reverse-proxy HTTPS protocol conversions on Render.
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
