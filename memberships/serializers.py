from rest_framework import serializers
from .models import Membership, MembershipRegistration
from users.serializers import UserSerializer, UserSimpleSerializer

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'name', 'description', 'benefits', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MembershipRegistrationSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    membership = MembershipSerializer(read_only=True)
    membership_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MembershipRegistration
        fields = [
            'id', 'user', 'user_id', 'membership', 'membership_id', 'start_date', 
            'is_active', 'status', 'payment_status', 'payment_amount', 'payment_method',
            'transaction_id', 'payment_date', 'reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['start_date', 'created_at', 'updated_at']

    def create(self, validated_data):
        return MembershipRegistration.objects.create(**validated_data)


class MembershipRegistrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    membership = MembershipSerializer(read_only=True)
    user = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = MembershipRegistration
        fields = ['id', 'user', 'membership', 'start_date', 'is_active', 'status', 'payment_status', 'reason']
