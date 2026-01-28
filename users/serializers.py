from rest_framework import  serializers
from .models import User
from django.contrib.auth import password_validation

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'name', 'email', 'role', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}, 
            'password_reset_token': {'read_only': True},  
            'password_reset_expires': {'read_only': True},  
            'last_login': {'read_only': True}, 
        }

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)  # Allow role to be specified during creation

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'role']

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data, password=password, role=role)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)  
    confirm_new_password = serializers.CharField(required=True, min_length=6)  

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match")
        return data
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_new_password = serializers.CharField(required=True, min_length=8)
    reset_token = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
