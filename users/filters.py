import django_filters
from django.db.models import Q
from .models import User

class UserFilter(django_filters.FilterSet):
    is_staff = django_filters.BooleanFilter(field_name='is_staff')
    is_superuser = django_filters.BooleanFilter(field_name='is_superuser')
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = User
        fields = ['is_staff', 'is_superuser', 'name']

    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(email__icontains=value)
        )