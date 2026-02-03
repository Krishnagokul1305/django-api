from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Membership, MembershipRegistration
from .serializers import (
    MembershipSerializer, 
    MembershipRegistrationSerializer,
    MembershipRegistrationListSerializer
)
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


class MembershipRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipRegistrationSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_status', 'is_active', 'user']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return MembershipRegistration.objects.all()
        return MembershipRegistration.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsStaffOrSuperAdmin()]

    def get_serializer_class(self):
        if self.action == 'list':
            return MembershipRegistrationListSerializer
        return MembershipRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new membership registration"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Ensure user is set correctly"""
        if not serializer.validated_data.get('user_id'):
            serializer.validated_data['user_id'] = self.request.user.id
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def renew(self, request, pk=None):
        """Renew a membership registration"""
        registration = self.get_object()
        from django.utils import timezone
        from datetime import timedelta
        
        # Get duration from membership or use default 30 days
        duration_days = 30
        new_expiry = timezone.now() + timedelta(days=duration_days)
        
        registration.expiry_date = new_expiry
        registration.renewal_count += 1
        registration.is_active = True
        registration.payment_status = 'pending'
        registration.save()
        
        return Response(
            {'message': 'Membership renewed successfully', 'new_expiry': registration.expiry_date},
            status=status.HTTP_200_OK
        )
