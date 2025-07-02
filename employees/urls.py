from django.urls import path

from employees.views import GameOrderList, GameOrderOwnedList

urlpatterns = [
    path('game-order-list', GameOrderList.as_view(), name='game-order-list'),
    path('game-order-list/owned/', GameOrderOwnedList.as_view(), name='owned-game-orders')
]
