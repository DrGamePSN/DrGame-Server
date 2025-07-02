from pyexpat.errors import messages

from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from accounts.auth import CustomJWTAuthentication
from accounts.permissions import IsEmployee
from employees.serializers import GameOrderSerializer, OrderListSerializer
from payments.models import GameOrder


# Create your views here.

# order filtering
class GameOrderList(generics.ListAPIView):
    queryset = GameOrder.objects.filter(status='in_progress')
    serializer_class = OrderListSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


class GameOrderOwnedList(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        # گرفتن کارمند متصل به کاربر احراز هویت‌شده
        user = self.request.user
        try:
            employee = user.employee
            return GameOrder.objects.filter(
                Q(account_setter=employee) | Q(data_uploader=employee)
            ).select_related('customer', 'order_type').prefetch_related('games')
        except AttributeError:
            return Response(status=400)


class GameOrderUnaccepted(generics.ListAPIView):
    queryset = GameOrder.objects.filter(status='payed')
    serializer_class = OrderListSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

# sony accounts

