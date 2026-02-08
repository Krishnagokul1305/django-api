from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Feedback
from .serializers import (
    FeedbackSerializer,
    FeedbackListSerializer,
    FeedbackCreateSerializer
)
from users.pagination import CustomPagination


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['feedback_type', 'user']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'list':
            return FeedbackListSerializer
        elif self.action == 'create':
            return FeedbackCreateSerializer
        return FeedbackSerializer

    def create(self, request, *args, **kwargs):
        """Submit feedback (users can only submit once per item)"""
        serializer = FeedbackCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Add user to validated data
        feedback = Feedback.objects.create(
            user=request.user,
            **serializer.validated_data
        )
        
        response_serializer = FeedbackSerializer(feedback)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
