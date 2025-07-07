from django.urls import path

from employees.views import EmployeePanelAcceptedGameOrderList, EmployeePanelOwnedGameOrderList, EmployeePanelSonyAccountByOrderGamesView, SonyAccountList

urlpatterns = [
    path('game-order-list/', EmployeePanelAcceptedGameOrderList.as_view(), name='game-order-list'),
    path('game-order-list/owned/', EmployeePanelOwnedGameOrderList.as_view(), name='owned-game-orders'),
    path('game-order-list/<int:order_id>/sony-accounts/', EmployeePanelSonyAccountByOrderGamesView.as_view(),
         name='sony-accounts-by-order-games'),
    path('sony-accounts/owned/', SonyAccountList.as_view(), name='sony-accounts'),
]
