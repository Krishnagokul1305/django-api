from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Internship, InternshipRegistration
from .serializers import (
    InternshipSerializer, 
    InternshipRegistrationSerializer,
    InternshipRegistrationListSerializer,
    InternshipApplicationReviewSerializer
)
from .filters import InternshipFilter
from users.pagination import CustomPagination
from users.permissions import IsStaffOrSuperAdmin

class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.filter()
    serializer_class = InternshipSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = InternshipFilter
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny] 
        else:
            permission_classes = [IsAuthenticated, IsStaffOrSuperAdmin]  
        return [permission() for permission in permission_classes]


class InternshipRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = InternshipRegistrationSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user', 'internship']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return InternshipRegistration.objects.all()
        return InternshipRegistration.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsStaffOrSuperAdmin()]

    def get_serializer_class(self):
        if self.action == 'list':
            return InternshipRegistrationListSerializer
        elif self.action in ['update_status', 'add_review']:
            return InternshipApplicationReviewSerializer
        return InternshipRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Apply for internship"""
        data = request.data.copy()
        data['user_id'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def update_status(self, request, pk=None):
        """Update application status"""
        registration = self.get_object()
        serializer = InternshipApplicationReviewSerializer(registration, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def add_review(self, request, pk=None):
        """Add review/feedback to application"""
        registration = self.get_object()
        serializer = InternshipApplicationReviewSerializer(registration, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsStaffOrSuperAdmin])
    def pending_applications(self, request):
        """Get all pending applications"""
        pending = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)
