from rest_framework.authentication import TokenAuthentication
from django.conf import settings

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get(getattr(settings, 'AUTH_TOKEN_COOKIE_NAME', 'auth_token'))
        if not token:
            return None
        return self.authenticate_credentials(token)