from rest_framework import serializers
from .models import Webinar, WebinarRegistration
from users.serializers import UserSerializer, UserSimpleSerializer
from core.utils import validate_image_file
from django.core.exceptions import ValidationError

class WebinarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Webinar
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


class WebinarRegistrationSerializer(serializers.ModelSerializer):
    webinar = WebinarSerializer(read_only=True)
    webinar_id = serializers.IntegerField(write_only=True)
    user = UserSimpleSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WebinarRegistration
        fields = [
            'id', 'webinar', 'webinar_id', 'user', 'user_id', 'registered_at', 
            'attended', 'attendance_marked_at', 'status', 'reason', 'rejection_reason', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['registered_at', 'attendance_marked_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        return WebinarRegistration.objects.create(**validated_data)


class WebinarRegistrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    webinar = WebinarSerializer(read_only=True)
    user = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = WebinarRegistration
        fields = ['id', 'webinar', 'user', 'registered_at', 'attended', 'status', 'reason']


class WebinarRegistrationAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for marking attendance only"""
    class Meta:
        model = WebinarRegistration
        fields = ['attended', 'attendance_marked_at']
        read_only_fields = ['attendance_marked_at']


class WebinarRejectionSerializer(serializers.ModelSerializer):
    """Serializer for rejection/cancellation with reason"""
    class Meta:
        model = WebinarRegistration
        fields = ['rejection_reason']


class WebinarRegistrationStatusSerializer(serializers.ModelSerializer):
    """Serializer for changing registration status"""
    
    class Meta:
        model = WebinarRegistration
        fields = ['rejection_reason']

    def validate(self, data):
        """Validate that rejection_reason is provided if status is being set to rejected"""
        # Get the status from context if available
        request = self.context.get('request')
        if request:
            new_status = request.data.get('status')
            if new_status == 'rejected' and not data.get('rejection_reason'):
                raise serializers.ValidationError({
                    'rejection_reason': 'Rejection reason is required when rejecting a registration.'
                })
        return data
