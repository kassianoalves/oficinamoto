from django.utils.deprecation import MiddlewareMixin

class CsrfExemptMiddleware(MiddlewareMixin):
    """
    Middleware to exempt /api/auth/* endpoints from CSRF validation.
    Exempts authentication endpoints from CSRF protection for API access.
    """
    
    def process_request(self, request):
        # Exempt all /api/auth/* paths from CSRF validation
        if request.path.startswith('/api/auth/'):
            request._dont_enforce_csrf_checks = True
        return None

