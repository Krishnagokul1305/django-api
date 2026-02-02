from rest_framework import serializers
from .models import Internship

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ['id', 'image', 'title', 'description', 'event_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
