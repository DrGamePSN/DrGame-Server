from django.urls import path

from employees.views import EmployeeListView

urlpatterns = [
    path('manager-panel/', EmployeeListView.as_view(), name='employee-list'),
]