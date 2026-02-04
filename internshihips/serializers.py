from rest_framework import serializers
from .models import Internship, InternshipRegistration
from users.serializers import UserSerializer
from core.utils import validate_image_file
from django.core.exceptions import ValidationError

class InternshipSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Internship
        fields = ['id', 'image', 'title', 'description', 'event_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_image(self, value):
        """Validate image file"""
        if value:
            try:
                validate_image_file(value)
            except ValidationError as e:
                raise serializers.ValidationError(str(e))
        return value


class InternshipRegistrationSerializer(serializers.ModelSerializer):
    internship = InternshipSerializer(read_only=True)
    internship_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = InternshipRegistration
        fields = [
            'id', 'internship', 'internship_id', 'user', 'user_id', 
            'resume_link', 'reason', 'status', 'applied_at', 'status_updated_at', 
            'rejection_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['applied_at', 'status_updated_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        return InternshipRegistration.objects.create(**validated_data)


class InternshipRegistrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    internship_title = serializers.CharField(source='internship.title', read_only=True)
    
    class Meta:
        model = InternshipRegistration
        fields = ['id', 'user_email', 'internship_title', 'status', 'applied_at', 'reason']


class InternshipApplicationReviewSerializer(serializers.ModelSerializer):
    """Serializer for admin/interviewer feedback"""
    class Meta:
        model = InternshipRegistration
        fields = ['status', 'rejection_reason']

