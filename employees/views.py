from django.db.models import Q, Count
from rest_framework import generics, status
from rest_framework.response import Response

from accounts.auth import CustomJWTAuthentication
from accounts.permissions import IsEmployee, restrict_access
from employees.serializers import EmployeeGameSerializer, GameOrderSerializer, EmployeeSonyAccountMatchedSerializer, \
    EmployeeSonyAccountSerializer, EmployeeTransactionSerializer
from payments.models import GameOrder, Transaction
from storage.models import SonyAccount, SonyAccountGame


# Create your views here.

# ==================== Personal Views ====================
class EmployeePanelAcceptedGameOrderList(generics.ListAPIView):
    queryset = GameOrder.objects.filter(status='in_progress')
    serializer_class = GameOrderSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


class EmployeePanelOwnedGameOrderList(generics.ListAPIView):
    serializer_class = GameOrderSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            return GameOrder.objects.filter(
                Q(account_setter=employee) | Q(data_uploader=employee)
            ).select_related('customer', 'order_type').prefetch_related('games')
        except AttributeError:
            return Response(status=400)


class EmployeePanelGameOrderUnacceptedList(generics.ListAPIView):
    queryset = GameOrder.objects.filter(status='payed')
    serializer_class = GameOrderSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


class EmployeePanelGameOrderDetail(generics.RetrieveAPIView):
    serializer_class = EmployeeGameSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            return GameOrder.objects.filter(
                Q(account_setter=employee) | Q(data_uploader=employee)
            ).select_related('customer', 'order_type').prefetch_related('games')
        except AttributeError:
            return Response(status=400)


class EmployeePanelSonyAccountByOrderGamesView(generics.ListAPIView):
    serializer_class = EmployeeSonyAccountMatchedSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        order_id = self.kwargs['order_id']

        try:
            order = GameOrder.objects.get(id=order_id, is_deleted=False)
        except GameOrder.DoesNotExist:
            return SonyAccount.objects.none()

        selected_games = order.games.all()

        queryset = SonyAccount.objects.filter(
            is_deleted=False,
            games__in=selected_games
        ).annotate(
            matching_games_count=Count('games')
        ).order_by('-matching_games_count')

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeePanelSonyAccountList(generics.ListAPIView):
    serializer_class = EmployeeSonyAccountSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            return SonyAccount.objects.filter(employee=employee)
        except AttributeError:
            return Response(status=404)


class EmployeePanelGetNewSonyAccount(generics.RetrieveAPIView):
    queryset = SonyAccount.objects.filter(is_owned=False, is_deleted=False)
    serializer_class = EmployeeSonyAccountSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self):
        try:
            oldest_account = self.queryset.order_by('created_at').first()
            if not oldest_account:
                return Response(
                    {"error": "هیچ حساب Sony با شرایط مورد نظر یافت نشد."},
                    status=status.HTTP_404_NOT_FOUND
                )
            if oldest_account.employee:
                unchecked_games = SonyAccountGame.objects.filter(
                    Q(account__employee=oldest_account.employee) & Q(is_checked=False)
                )
                if unchecked_games.exists():
                    return Response(
                        {"error": "شما حساب‌های بازی چک‌نشده دارید."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return oldest_account
        except SonyAccount.DoesNotExist:
            return Response(
                {"error": "هیچ حساب Sony با شرایط مورد نظر یافت نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # اگر پاسخ خطا باشد، مستقیماً برگردانده می‌شود
        if isinstance(instance, Response):
            return instance
        # سریالایز کردن و برگرداندن یوزرنیم و پسورد
        serializer = self.get_serializer(instance)
        return Response({
            "username": serializer.data["username"],
            "password": serializer.data["password"]
        })


# class MakePaymentLinkForSonyAccount(generics.RetrieveAPIView):
#     pass

class EmployeePanelOwnedTransactionList(generics.ListAPIView):
    serializer_class = EmployeeTransactionSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        receiver = self.request.user
        try:
            return Transaction.objects.filter(receiver=receiver, is_deleted=False)
        except AttributeError:
            return Response(status=404)
