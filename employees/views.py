from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction as db_transaction
from accounts.auth import CustomJWTAuthentication
from accounts.permissions import IsEmployee, restrict_access
from employees.filters import EmployeeTaskFilter
from employees.models import EmployeeTask
from employees.serializers import EmployeeGameSerializer, EmployeeGameOrderSerializer, \
    EmployeeSonyAccountMatchedSerializer, \
    EmployeeSonyAccountSerializer, EmployeeTransactionSerializer, EmployeeProductSerializer, \
    EmployeeTaskSerializer, EmployeeProductOrderSerializer, EmployeeRepairOrderSerializer
from payments.models import GameOrder, Transaction, Order
from storage.models import SonyAccount, SonyAccountGame, Product


# Create your views here.

# ==================== Personal Views ====================
# -------------------- sony-accounts --------------------
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


class EmployeePanelSonyAccountDetail(generics.RetrieveUpdateDestroyAPIView):
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


# -------------------- orders --------------------
class EmployeePanelOwnedGameOrderList(generics.ListAPIView):
    serializer_class = EmployeeGameOrderSerializer
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
            return Response(status=404)


# -------------------- tasks --------------------
class EmployeePanelTaskList(generics.ListAPIView):
    serializer_class = EmployeeTaskSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeTaskFilter

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            return EmployeeTask.objects.filter(employee=employee)
        except AttributeError:
            return Response(status=404)


class EmployeePanelTaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeTaskSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            return EmployeeTask.objects.filter(employee=employee)
        except AttributeError:
            return Response(status=404)


class EmployeePanelAddTask(generics.CreateAPIView):
    serializer_class = EmployeeTaskSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            return EmployeeTask.objects.filter(employee=employee)
        except AttributeError:
            return Response(status=404)


# -------------------- transactions --------------------
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


class EmployeePanelOwnedTransactionDetail(generics.RetrieveAPIView):
    serializer_class = EmployeeTransactionSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        receiver = self.request.user
        try:
            return Transaction.objects.filter(receiver=receiver, is_deleted=False)
        except AttributeError:
            return Response(status=404)


# ==================== Product Views ====================
@restrict_access('has_access_to_products')
class EmployeePanelProductList(generics.ListAPIView):
    serializer_class = EmployeeProductSerializer
    queryset = Product.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_products')
class EmployeePanelProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeProductSerializer
    queryset = Product.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_products')
class EmployeePanelAddProduct(generics.CreateAPIView):
    serializer_class = EmployeeProductSerializer
    queryset = Product.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


# ==================== SonyAccounts Views ====================
@restrict_access('has_access_to_accounts')
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
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance)
        return Response({
            "username": serializer.data["username"],
            "password": serializer.data["password"]
        })


# ==================== ProductOrders Views ====================
@restrict_access('has_access_to_orders')
class EmployeePanelProductOrderList(generics.ListAPIView):
    serializer_class = EmployeeProductOrderSerializer
    queryset = Order.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_orders')
class EmployeePanelProductOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeProductOrderSerializer
    queryset = Order.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_orders')
class EmployeePanelAddOrder(generics.CreateAPIView):
    serializer_class = EmployeeProductOrderSerializer
    queryset = Order.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


# ==================== AccountOrders Views ====================
@restrict_access('has_access_to_game_order')
class EmployeePanelAcceptedGameOrderList(generics.ListAPIView):
    queryset = GameOrder.objects.filter(status='in_progress')
    serializer_class = EmployeeGameOrderSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_game_order')
class EmployeePanelGameOrderUnacceptedList(generics.ListAPIView):
    queryset = GameOrder.objects.filter(status='payed')
    serializer_class = EmployeeGameOrderSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_game_order')
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


# ==================== RepairOrders Views ====================
@restrict_access('has_access_to_orders')
class EmployeePanelRepairOrderList(generics.ListAPIView):
    serializer_class = EmployeeRepairOrderSerializer
    queryset = Order.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_orders')
class EmployeePanelRepairOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeRepairOrderSerializer
    queryset = Order.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_orders')
class EmployeePanelAddRepairOrder(generics.CreateAPIView):
    serializer_class = EmployeeRepairOrderSerializer
    queryset = Order.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


# ==================== Transactions Views ====================
@restrict_access('has_access_to_transactions')
class EmployeePanelTransactionList(generics.ListAPIView):
    serializer_class = EmployeeTransactionSerializer
    queryset = Transaction.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_transactions')
class EmployeePanelTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeTransactionSerializer
    queryset = Transaction.objects.filter(is_deleted=False)
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]


@restrict_access('has_access_to_transactions')
class EmployeePanelAddTransaction(generics.CreateAPIView):
    serializer_class = EmployeeTransactionSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def perform_create(self, serializer):
        try:
            with db_transaction.atomic():
                validated_data = serializer.validated_data
                payer = validated_data.get('payer')
                receiver = validated_data.get('receiver')
                amount = validated_data['amount']

                if payer:
                    if payer.balance < amount:
                        return Response({"detail": "موجودی payer کافی نیست."}, status=400)
                    payer.balance -= amount
                    payer.save()
                if receiver:
                    receiver.balance += amount
                    receiver.save()
                serializer.save()
        except AttributeError:
            return Response({"detail": "کاربر مرتبط یافت نشد."}, status=404)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)
