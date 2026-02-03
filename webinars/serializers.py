from rest_framework import serializers
from .models import Webinar, WebinarRegistration
from users.serializers import UserSerializer

class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = ['id', 'image', 'title', 'description', 'event_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class WebinarRegistrationSerializer(serializers.ModelSerializer):
    webinar = WebinarSerializer(read_only=True)
    webinar_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WebinarRegistration
        fields = [
            'id', 'webinar', 'webinar_id', 'user', 'user_id', 'registered_at', 
            'attended', 'attendance_marked_at', 'rating', 'feedback', 'feedback_given_at',
            'rejection_reason', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['registered_at', 'attendance_marked_at', 'feedback_given_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        return WebinarRegistration.objects.create(**validated_data)


class WebinarRegistrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    webinar_title = serializers.CharField(source='webinar.title', read_only=True)
    
    class Meta:
        model = WebinarRegistration
        fields = ['id', 'user_email', 'webinar_title', 'registered_at', 'attended', 'rating']


class WebinarRegistrationAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for marking attendance only"""
    class Meta:
        model = WebinarRegistration
        fields = ['attended', 'attendance_marked_at']
        read_only_fields = ['attendance_marked_at']


class WebinarFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for user feedback submission (once only per event)"""
    
    class Meta:
        model = WebinarRegistration
        fields = ['rating', 'feedback', 'feedback_given_at']
        read_only_fields = ['feedback_given_at']

    def validate(self, data):
        """Ensure feedback hasn't already been given"""
        if self.instance and self.instance.feedback_given_at:
            raise serializers.ValidationError("Feedback has already been submitted for this webinar registration.")
        return data


class WebinarRejectionSerializer(serializers.ModelSerializer):
    """Serializer for rejection/cancellation with reason"""
    class Meta:
        model = WebinarRegistration
        fields = ['rejection_reason', 'notes']


class WebinarRegistrationStatusSerializer(serializers.ModelSerializer):
    """Serializer for changing registration status"""
    
    class Meta:
        model = WebinarRegistration
        fields = ['rejection_reason', 'notes']

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
