from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import CreateUserSerializer
from .serializers import ChangePasswordSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,VerifyEmailSerializer
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

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
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "No user is associated with this email address."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.generate_password_reset_token()
            frontend = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            reset_path = f"/reset-password/?token={user.password_reset_token}"
            reset_link = frontend.rstrip('/') + reset_path

            html_content = render_to_string('emails/resetpassword.html', {
                'user_name': getattr(user, 'name', user.email),
                'user_email': user.email,
                'reset_link': reset_link,
                'dashboard_url': frontend.rstrip('/') + '/dashboard',
            })

            # message = EmailMessage(
            #     subject="Password reset request",
            #     body=html_content,
            #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            #     to=[user.email],
            # )

            # message.content_subtype = "html"
            # message.send(fail_silently=False)
            return Response({"token": user.password_reset_token}, status=status.HTTP_200_OK)

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

class UserRegisterAPI(APIView):
    def post(self, request):
        data = request.data.copy()
        data['is_staff'] = False  

        email = data.get('email')
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            if existing_user.is_active:
                return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

            existing_user.generate_email_verification_token()

            # html_content = render_to_string('emails/emailverification.html', {
            #     'user_name': getattr(existing_user, 'name', existing_user.email),
            #     'verification_url': getattr(settings, 'FRONTEND_URL', 'http://localhost:3000').rstrip('/') + f"/verify-email/?token={existing_user.email_verification_token}",
            # })

            # message = EmailMessage(
            #     subject="Verify your email",
            #     body=html_content,
            #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            #     to=[existing_user.email],
            # )

            # message.content_subtype = "html"
            # message.send(fail_silently=False)
            return Response({"message": "verification_resent"}, status=status.HTTP_200_OK)

        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            # user.is_active = False
            user.generate_email_verification_token()
            user.save()

            # html_content = render_to_string('emails/emailverification.html', {
            #     'user_name': getattr(user, 'name', user.email),
            #     'verification_url': getattr(settings, 'FRONTEND_URL', 'http://localhost:3000').rstrip('/') + f"/verify-email/?token={user.email_verification_token}",
            # })

            # message = EmailMessage(
            #     subject="Verify your email",
            #     body=html_content,
            #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            #     to=[user.email],
            # )

            # message.content_subtype = "html"
            # message.send(fail_silently=False)
            return Response({"message": "created"}, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPI(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['verification_token']

            try:
                user = User.objects.get(email_verification_token=token)
            except User.DoesNotExist:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            if user.email_verification_expires and user.email_verification_expires < timezone.now():
                return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.email_verification_token = None
            user.email_verification_expires = None
            user.save()

            # html_content = render_to_string('emails/welcomeuser.html', {
            #     'user_name': getattr(user, 'name', user.email),
            #     'email': user.email,
            # })

            # message = EmailMessage(
            #     subject="Welcome to Liture",
            #     body=html_content,
            #     from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            #     to=[user.email],
            # )

            # message.content_subtype = "html"
            # message.send(fail_silently=False)
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
