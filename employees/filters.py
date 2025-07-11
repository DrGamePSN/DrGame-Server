# your_app/filters.py
from employees.models import EmployeeTask
from django_filters import rest_framework as filters


class EmployeeTaskFilter(filters.FilterSet):
    type = filters.ChoiceFilter(choices=EmployeeTask._meta.get_field('type').choices)
    status = filters.ChoiceFilter(choices=EmployeeTask._meta.get_field('status').choices)
    deadline__gte = filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')
    deadline__lte = filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = EmployeeTask
        fields = ['type', 'status', 'deadline__gte', 'deadline__lte', 'title']