import django_filters
from .models import Membership

class MembershipFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # partial search
    description = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    created_at = django_filters.DateFromToRangeFilter()  # filter by date range

    class Meta:
        model = Membership
        fields = ['name', 'description', 'is_active', 'created_at']
