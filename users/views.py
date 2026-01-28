from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserListSerializer,CreateUserSerializer,ChangePasswordSerializer,ForgotPasswordSerializer,ResetPasswordSerializer
from rest_framework import status 
from .permissions import IsSuperAdmin,IsOwner
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class UserListAPI(APIView):
    permission_classes=[IsAuthenticated,IsSuperAdmin]
    def get(self,request):
        users=User.objects.all()
        serialized_users=UserListSerializer(users,many=True)
        return Response({"data":serialized_users.data})
    
    def post(self,request):
        serialized_data=CreateUserSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({"message":"User created successfully"})
        else:
            return Response({"errors":serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPI(APIView):
    permission_classes=[IsOwner]
    def get(self,request,id):
        try:
            user=User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
        serialized_user=UserListSerializer(user)
        return Response({"data":serialized_user.data})
    
    def delete(self,request,id):
        try:
            user=User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self,request,id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,user)
        serializer = CreateUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data})
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class UserChangePasswordAPI(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,id):
        user=request.user
        if user.id != id:  
            return Response({"error": "You cannot change another user's password"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save() 
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordAPI(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if the user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "No user is associated with this email address."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate password reset token using the model's method
            user.generate_password_reset_token()

            reset_link = f"/reset-password/?token={user.password_reset_token}"  # Assuming your frontend handles this URL
            # send_mail(
            #     "Password Reset Request",
            #     f"Click the link below to reset your password:\n\n{reset_link}",
            #     settings.DEFAULT_FROM_EMAIL,
            #     [email]
            # )

            return Response({"message": "Password reset link has been sent to your email.","token":reset_link}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordAPI(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(password_reset_token=reset_token)
            except User.DoesNotExist:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            if user.password_reset_expires < timezone.now():
                return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user.reset_password(new_password)

            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserListSerializer(user)
        return Response({"data":serializer.data})