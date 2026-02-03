from rest_framework import serializers
from .models import Membership, MembershipRegistration
from users.serializers import UserSerializer

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'name', 'description', 'benefits', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MembershipRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    membership = MembershipSerializer(read_only=True)
    membership_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MembershipRegistration
        fields = [
            'id', 'user', 'user_id', 'membership', 'membership_id', 'start_date', 'expiry_date', 
            'is_active', 'renewal_count', 'payment_status', 'payment_amount', 'payment_method',
            'transaction_id', 'payment_date', 'reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['start_date', 'created_at', 'updated_at']

    def create(self, validated_data):
        return MembershipRegistration.objects.create(**validated_data)


class MembershipRegistrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    membership_name = serializers.CharField(source='membership.name', read_only=True)
    
    class Meta:
        model = MembershipRegistration
        fields = ['id', 'user_email', 'membership_name', 'start_date', 'expiry_date', 'is_active', 'payment_status', 'reason']
