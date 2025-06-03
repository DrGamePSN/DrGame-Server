from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # اول چک کن کوکی
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        if access_token:
            try:
                # اعتبارسنجی توکن
                validated_token = self.get_validated_token(access_token)
                user = self.get_user(validated_token)
                print(f"Valid token for user: {user.id}")
                return (user, validated_token)
            except (InvalidToken, AuthenticationFailed):
                return None

        # اگه کوکی نبود، به روش استاندارد (Bearer) ادامه بده
        return super().authenticate(request)