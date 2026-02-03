from rest_framework import  serializers
from .models import User
from django.contrib.auth import password_validation

class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for nested usage"""
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone_number', 'is_staff', 'is_superuser', 'is_active']
        read_only_fields = ['id']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'name', 'email', 'phone_number', 'is_staff', 'is_superuser', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}, 
            'password_reset_token': {'read_only': True},  
            'password_reset_expires': {'read_only': True},  
            'last_login': {'read_only': True}, 
        }

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    is_staff = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'phone_number', 'is_staff']

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate(self, data):
        request = self.context.get('request')
        is_staff = data.get('is_staff', False)
        
        if request and request.user.is_authenticated:
            # If user is trying to create staff, they must be superuser
            if is_staff and not request.user.is_superuser:
                raise serializers.ValidationError("Only superusers can create staff users")
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        is_staff = validated_data.pop('is_staff', False)
        user = User.objects.create_user(**validated_data, password=password)
        user.is_staff = is_staff
        user.save()
        return user
