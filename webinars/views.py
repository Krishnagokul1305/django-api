from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Webinar
from .serializers import WebinarSerializer
from .filters import WebinarFilter
from users.pagination import CustomPagination
from users.permissions import IsStaffOrSuperAdmin

class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.filter()
    serializer_class = WebinarSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WebinarFilter

    # Dynamic permissions
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsStaffOrSuperAdmin]
        return [permission() for permission in permission_classes]
