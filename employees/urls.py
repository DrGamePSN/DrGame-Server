from django.urls import path
from employees import views

urlpatterns = [
    # ==================== Personal Views ====================
    # -------------------- Sony Accounts --------------------
    path('personal/sony-accounts/', views.EmployeePanelOwnedSonyAccountList.as_view(), name='owned-sony-account-list'),
    path('personal/sony-accounts/<int:pk>/', views.EmployeePanelSonyAccountDetail.as_view(),
         name='sony-account-detail'),
    path('personal/sony-accounts/order/<int:order_id>/', views.EmployeePanelSonyAccountByOrderGamesView.as_view(),
         name='sony-account-by-order-games'),

    # -------------------- Orders --------------------
    path('personal/game-orders/owned/', views.EmployeePanelOwnedGameOrderList.as_view(), name='owned-game-order-list'),

    # -------------------- Tasks --------------------
    path('personal/tasks/', views.EmployeePanelTaskList.as_view(), name='task-list'),
    path('personal/tasks/<int:pk>/', views.EmployeePanelTaskDetail.as_view(), name='task-detail'),
    path('personal/tasks/add/', views.EmployeePanelAddTask.as_view(), name='task-add'),

    # -------------------- Transactions --------------------
    path('personal/transactions/owned/', views.EmployeePanelOwnedTransactionList.as_view(),
         name='owned-transaction-list'),
    path('personal/transactions/owned/<int:pk>/', views.EmployeePanelOwnedTransactionDetail.as_view(),
         name='owned-transaction-detail'),

    # ==================== Product Views ====================
    path('products/', views.EmployeePanelProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.EmployeePanelProductDetail.as_view(), name='product-detail'),
    path('products/add/', views.EmployeePanelAddProduct.as_view(), name='product-add'),

    # ==================== SonyAccounts Views ====================
    path('sony-accounts/new/', views.EmployeePanelGetNewSonyAccount.as_view(), name='sony-account-new'),
    path('sony-accounts/', views.EmployeePanelSonyAccountList.as_view(), name='sony-account-list'),

    # ==================== ProductOrders Views ====================
    path('product-orders/', views.EmployeePanelProductOrderList.as_view(), name='product-order-list'),
    path('product-orders/<int:pk>/', views.EmployeePanelProductOrderDetail.as_view(), name='product-order-detail'),
    path('product-orders/add/', views.EmployeePanelAddOrder.as_view(), name='product-order-add'),

    # ==================== AccountOrders Views ====================
    path('game-orders/', views.EmployeePanelGameOrderList.as_view(), name='accepted-game-order-list'),
    path('game-orders/<int:pk>/', views.EmployeePanelGameOrderDetail.as_view(), name='game-order-detail'),

    # ==================== RepairOrders Views ====================
    path('repair-orders/', views.EmployeePanelRepairOrderList.as_view(), name='repair-order-list'),
    path('repair-orders/<int:pk>/', views.EmployeePanelRepairOrderDetail.as_view(), name='repair-order-detail'),

    # ==================== Transactions Views ====================
    path('transactions/', views.EmployeePanelTransactionList.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.EmployeePanelTransactionDetail.as_view(), name='transaction-detail'),
    path('transactions/add/', views.EmployeePanelAddTransaction.as_view(), name='transaction-add'),
]
