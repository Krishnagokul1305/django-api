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
    filterset_fields = ['payment_status', 'is_active', 'user', 'status']

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

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def change_status(self, request, pk=None):
        """
        Change membership registration status.
        Required fields: status (accepted/rejected/pending)
        If status is 'rejected', rejection_reason is required.
        """
        registration = self.get_object()
        new_status = request.data.get('status')
        rejection_reason = request.data.get('rejection_reason')
        
        valid_statuses = ['pending', 'accepted', 'rejected']
        if not new_status:
            return Response(
                {'error': 'Status field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Require rejection reason when rejecting
        if new_status == 'rejected' and not rejection_reason:
            return Response(
                {'error': 'Rejection reason is required when setting status to rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update the status manually
        registration.status = new_status
        
        # Update rejection reason if provided
        if rejection_reason:
            registration.rejection_reason = rejection_reason
        
        registration.save()
        
        response_data = MembershipRegistrationSerializer(registration).data
        response_data['message'] = f'Membership status changed to {new_status}'
        
        return Response(response_data, status=status.HTTP_200_OK)
