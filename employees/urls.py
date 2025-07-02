from django.urls import path

from employees.views import GameOrderList, GameOrderOwnedList, SonyAccountByOrderGamesView, SonyAccountList

urlpatterns = [
    path('game-order-list', GameOrderList.as_view(), name='game-order-list'),
    path('game-order-list/owned/', GameOrderOwnedList.as_view(), name='owned-game-orders'),
    path('game-order-list/<int:order_id>/sony-accounts/', SonyAccountByOrderGamesView.as_view(),
         name='sony-accounts-by-order-games'),
    path('sony-accounts/owned/', SonyAccountList.as_view(), name='sony-accounts'),
]
