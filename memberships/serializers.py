from rest_framework import serializers
from .models import Membership

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'name', 'description', 'benefits', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
