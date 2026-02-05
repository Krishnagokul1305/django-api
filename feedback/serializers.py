from rest_framework import serializers
from .models import Feedback
from users.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'user_id', 'content_type', 'object_id', 'feedback_type',
            'rating', 'comment', 'submitted_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['submitted_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Feedback.objects.create(**validated_data)


class FeedbackListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'user_name', 'user_email', 'content_type_name', 'object_id',
            'feedback_type', 'rating', 'submitted_at'
        ]


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """Serializer for user feedback submission"""
    
    class Meta:
        model = Feedback
        fields = ['content_type', 'object_id', 'feedback_type', 'rating', 'comment']

    def validate(self, data):
        """Ensure feedback hasn't already been given for this object"""
        user = self.context['request'].user
        content_type = data.get('content_type')
        object_id = data.get('object_id')
        
        if Feedback.objects.filter(
            user=user,
            content_type=content_type,
            object_id=object_id
        ).exists():
            raise serializers.ValidationError(
                "You have already submitted feedback for this item."
            )
        return data
