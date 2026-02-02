from rest_framework import serializers
from .models import Webinar

class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = ['id', 'image', 'title', 'description', 'event_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
