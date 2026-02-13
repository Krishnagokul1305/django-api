from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Webinar, WebinarRegistration
from .serializers import (
    WebinarSerializer, 
    WebinarRegistrationSerializer,
    WebinarRegistrationListSerializer,
    WebinarRegistrationAttendanceSerializer,
    WebinarRejectionSerializer,
    WebinarRegistrationStatusSerializer
)
from .filters import WebinarFilter
from users.pagination import CustomPagination
from users.permissions import IsStaffOrSuperAdmin
from django.utils import timezone

class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.filter()
    serializer_class = WebinarSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WebinarFilter
    parser_classes = (MultiPartParser, FormParser)

    # Dynamic permissions
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsStaffOrSuperAdmin]
        return [permission() for permission in permission_classes]

class WebinarRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = WebinarRegistrationSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['attended', 'user', 'webinar', 'status']
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return WebinarRegistration.objects.all()
        return WebinarRegistration.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsStaffOrSuperAdmin()]

    def get_serializer_class(self):
        if self.action == 'list':
            return WebinarRegistrationListSerializer
        elif self.action == 'mark_attendance':
            return WebinarRegistrationAttendanceSerializer
        elif self.action == 'reject':
            return WebinarRejectionSerializer
        elif self.action == 'change_status':
            return WebinarRegistrationStatusSerializer
        return WebinarRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Register user for a webinar"""
        data = request.data.copy()
        webinar_id = data.get('webinar_id')
        if webinar_id and WebinarRegistration.objects.filter(
            webinar_id=webinar_id, user_id=request.user.id
        ).exists():
            return Response(
                {"error": "You have already registered for this webinar."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        registration = serializer.instance
        user = registration.user
        html_content = render_to_string('emails/registration.html', {
            'user_name': getattr(user, 'name', user.email),
            'title': registration.webinar.title,
            'type': 'Webinar',
            'email': user.email,
            'current_year': timezone.now().year,
        })

        # message = EmailMessage(
        #     subject="Registration received",
        #     body=html_content,
        #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        #     to=[user.email],
        # )

        # message.content_subtype = "html"
        # message.send(fail_silently=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Ensure user is set correctly"""
        if not serializer.validated_data.get('user_id'):
            serializer.validated_data['user_id'] = self.request.user.id
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def mark_attendance(self, request, pk=None):
        """Mark attendance for a webinar registration"""
        registration = self.get_object()
        serializer = WebinarRegistrationAttendanceSerializer(registration, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Update attendance_marked_at if marking as attended
        if serializer.validated_data.get('attended'):
            registration.attendance_marked_at = timezone.now()
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def reject(self, request, pk=None):
        """
        Reject/Cancel registration with reason.
        Required fields: rejection_reason
        """
        registration = self.get_object()
        serializer = WebinarRejectionSerializer(registration, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {**serializer.data, 'message': 'Registration rejected/cancelled'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def change_status(self, request, pk=None):
        """
        Change registration status.
        Required fields: status (accepted/rejected/cancelled/pending)
        If status is 'rejected', rejection_reason is required.
        """
        registration = self.get_object()
        new_status = request.data.get('status')
        rejection_reason = request.data.get('rejection_reason')
        
        valid_statuses = ['accepted', 'rejected', 'cancelled', 'pending']
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
        
        registration.status = new_status
        
        if rejection_reason:
            registration.rejection_reason = rejection_reason
        
        registration.save()

        if registration.status in ['accepted', 'rejected']:
            user = registration.user
            html_content = render_to_string('emails/registrationStatus.html', {
                'user_name': getattr(user, 'name', user.email),
                'title': registration.webinar.title,
                'type': 'Webinar',
                'status': registration.status,
                'rejection_reason': registration.rejection_reason or '',
            })

            # message = EmailMessage(
            #     subject="Application status updated",
            #     body=html_content,
            #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            #     to=[user.email],
            # )

            # message.content_subtype = "html"
            # message.send(fail_silently=False)

        response_data = WebinarRegistrationSerializer(registration).data
        response_data['message'] = f'Registration status changed to {new_status}'
        
        return Response(response_data, status=status.HTTP_200_OK)
