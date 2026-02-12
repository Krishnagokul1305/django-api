from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .tasks import (
    send_membership_registration_email,
    send_membership_status_email,
)
from .models import Membership, MembershipRegistration
from .serializers import (
    MembershipSerializer, 
    MembershipRegistrationSerializer,
    MembershipRegistrationListSerializer
)
from .filters import MembershipFilter
from users.pagination import CustomPagination
from users.permissions import IsStaffOrSuperAdmin
from django.utils import timezone

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
        data = request.data.copy()
        membership_id = data.get('membership_id')
        if membership_id and MembershipRegistration.objects.filter(
            membership_id=membership_id, user_id=request.user.id
        ).exists():
            return Response(
                {"error": "You have already registered for this membership."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        registration = serializer.instance
        user = registration.user
        send_membership_registration_email.delay(
            getattr(user, 'name', user.email),
            user.email,
            registration.membership.name,
            timezone.now().year,
        )
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

        if registration.status in ['accepted', 'rejected']:
            user = registration.user
            send_membership_status_email.delay(
                getattr(user, 'name', user.email),
                user.email,
                registration.membership.name,
                registration.status,
                registration.rejection_reason or '',
            )

        response_data = MembershipRegistrationSerializer(registration).data
        response_data['message'] = f'Membership status changed to {new_status}'
        
        return Response(response_data, status=status.HTTP_200_OK)
