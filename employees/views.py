from django.db.models import Q, Count
from rest_framework import generics
from rest_framework.response import Response

from accounts.auth import CustomJWTAuthentication
from accounts.permissions import IsEmployee, restrict_access
from employees.serializers import EmployeeGameSerializer, GameOrderSerializer, EmployeeSonyAccountSerializer
from payments.models import GameOrder
from storage.models import SonyAccount


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
    serializer_class = EmployeeSonyAccountSerializer
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


class EmployeeSonyAccountList(generics.ListAPIView):
    serializer_class = EmployeeSonyAccountSerializer
    permission_classes = [IsEmployee]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            return SonyAccount.objects.filter(employee=employee)
        except AttributeError:
            return Response(status=400)

