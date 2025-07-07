from django.urls import path

from employees.views import EmployeePanelAcceptedGameOrderList, EmployeePanelOwnedGameOrderList, \
    EmployeePanelSonyAccountByOrderGamesView, EmployeePanelSonyAccountList, EmployeePanelGetNewSonyAccount, \
    EmployeePanelOwnedTransactionList

urlpatterns = [
    path('game-order/list/', EmployeePanelAcceptedGameOrderList.as_view(), name='game-order-list'),
    path('game-order/list/owned/', EmployeePanelOwnedGameOrderList.as_view(), name='owned-game-orders'),
    path('game-order/list/<int:order_id>/sony-accounts/', EmployeePanelSonyAccountByOrderGamesView.as_view(),
         name='sony-accounts-by-order-games'),
    path('sony-accounts/owned/', EmployeePanelSonyAccountList.as_view(), name='sony-accounts'),
    path('sony-accounts/get-new/', EmployeePanelGetNewSonyAccount.as_view(), name='get-new-sony-account'),
    path('transactions/owned/', EmployeePanelOwnedTransactionList.as_view(), name='owned-transactions'),

]
