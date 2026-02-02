from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Membership
from .serializers import MembershipSerializer
from .filters import MembershipFilter
from users.pagination import CustomPagination
from users.permissions import IsStaffOrSuperAdmin

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.filter()
    serializer_class = MembershipSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MembershipFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]  # Read access for everyone
        else:
            permission_classes = [IsAuthenticated, IsStaffOrSuperAdmin]  # Staff only
        return [permission() for permission in permission_classes]
