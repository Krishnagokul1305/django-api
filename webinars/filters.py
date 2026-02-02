import django_filters
from .models import Webinar

class WebinarFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')  # partial search
    description = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    event_date = django_filters.DateFromToRangeFilter()  # filter by date range
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Webinar
        fields = ['title', 'description', 'is_active', 'event_date', 'created_at']
