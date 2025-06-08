# your_app/views.py
import secrets
from datetime import timedelta
import requests
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from DrGame import settings
from accounts.auth import CustomJWTAuthentication
from accounts.models import CustomUser, OTP, APIKey, MainManager
from accounts.throttles import PhoneRateThrottle
from customers.models import Customer, BusinessCustomer
from employees.models import Employee, Repairman


class CreateAPIKeyView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        client_name = request.data.get('client_name')

        if not phone or not password or not client_name:
            return Response(
                {"error": "شماره موبایل، رمز عبور و نام کلاینت الزامی است"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(phone=phone, password=password)
        if not user or not user.is_superuser:
            return Response(
                {"error": "فقط سوپریوزرها می‌توانند API Key تولید کنند"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        api_key = APIKey.objects.create(client_name=client_name)

        return Response(
            {
                "api_key": api_key.key,
                "client_name": api_key.client_name
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        return Response(
            {"error": "فقط متد POST پشتیبانی می‌شود"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class RequestOTPView(APIView):
    throttle_classes = [AnonRateThrottle, PhoneRateThrottle]

    def post(self, request):
        # چک کردن API Key
        api_key = request.headers.get('X-API-Key')
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            return Response(
                {"error": "API Key نامعتبر است"},
                status=status.HTTP_403_FORBIDDEN
            )

        phone = request.data.get('phone')
        if not phone:
            return Response(
                {"error": "شماره موبایل الزامی است"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = CustomUser.objects.get_or_create(phone=phone, defaults={'is_active': True})
        otp_code = str(secrets.randbelow(100000000)).zfill(8)
        expires_at = timezone.now() + timedelta(minutes=2)
        OTP.objects.create(user=user, code=otp_code, expires_at=expires_at)
        faraz_url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
        faraz_api_key = "OWYwNmNlODYtNTc2YS00OTEzLWIzZmMtYWFiNzQxOGIyN2Y1NzMzZmNiOGI2ODMyZmY1Y2JhZWNjNzVlNWNhOGMyOWU="
        faraz_phone = '+98' + phone[1:]
        headers = {
            "apikey": faraz_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "code": "0li89sh8n64thu4",
            "sender": "+983000505",
            "recipient": faraz_phone,
            "variable": {
                "code": otp_code
            }
        }
        try:
            response = requests.post(faraz_url, json=payload, headers=headers, timeout=10)
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Body: {response.text}")
            try:
                print(f"Response JSON: {response.json()}")
            except ValueError:
                print("Response is not valid JSON")

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
        print(f"OTP for {phone}: {otp_code}")
        return Response(
            {"message": "لطفاً کد OTP را وارد کنید"},
            status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            return Response(
                {"error": "Invalid API Key"},
                status=status.HTTP_403_FORBIDDEN
            )

        phone = request.data.get('phone')
        code = request.data.get('code')
        if not phone or not code:
            return Response(
                {"error": "Phone number and OTP code are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otp = OTP.objects.filter(user=user).latest('created_at')
            if otp.code != code or not otp.is_valid():
                return Response(
                    {"error": "Invalid or expired OTP"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except OTP.DoesNotExist:
            return Response(
                {"error": "No OTP found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            {"message": "Login successful"},
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=3600,
            path='/',
            domain='localhost'  # برای لوکال
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=432000,
            path='/',
            domain='localhost'
        )

        return response


class RefreshTokenView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            return Response(
                {"error": "Invalid API Key"},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "No refresh token provided"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response(
                {"message": "Token refreshed successfully"},
                status=status.HTTP_200_OK
            )
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],  # False برای توسعه
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],  # Lax برای توسعه
                max_age=3600
            )

            if hasattr(refresh, 'token'):
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],  # False برای توسعه
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],  # Lax برای توسعه
                    max_age=432000
                )

            return response

        except TokenError as e:
            return Response(
                {"error": f"Invalid refresh token: {str(e)}"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request):  # اضافه کردن متد GET
        return self.post(request)  # استفاده از منطق POST

    def post(self, request):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            return Response(
                {"error": "Invalid API Key"},
                status=status.HTTP_403_FORBIDDEN
            )

        response = Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class UserStatusView(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {
                    "is_authenticated": False,
                    "user_type": None,
                    "user_id": None
                },
                status=200
            )

        user = request.user
        user_type = None

        if MainManager.objects.filter(user=user).exists():
            user_type = "main_manager"
        elif Employee.objects.filter(user=user).exists():
            user_type = "employee"
        elif Repairman.objects.filter(user=user).exists():
            user_type = "repairman"
        elif Customer.objects.filter(user=user).exists():
            user_type = "customer"
        elif BusinessCustomer.objects.filter(user=user).exists():
            user_type = "business_customer"
        else:
            user_type = "none"

        return Response(
            {
                "is_authenticated": True,
                "user_type": user_type,
                "user_id": user.id
            },
            status=200
        )
