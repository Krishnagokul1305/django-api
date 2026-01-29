from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserListSerializer,CreateUserSerializer
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
        

class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserListSerializer(user)
        return Response({"data":serializer.data})