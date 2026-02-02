from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Internship
from .serializers import InternshipSerializer
from .filters import InternshipFilter
from users.pagination import CustomPagination
from users.permissions import IsStaffOrSuperAdmin

class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.filter()
    serializer_class = InternshipSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = InternshipFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny] 
        else:
            permission_classes = [IsAuthenticated, IsStaffOrSuperAdmin]  
        return [permission() for permission in permission_classes]
