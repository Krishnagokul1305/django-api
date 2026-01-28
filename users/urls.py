from django.urls import path
from .views import UserListAPI,UserDetailAPI,UserChangePasswordAPI,ForgotPasswordAPI,ResetPasswordAPI,UserProfileView

urlpatterns=[
path("",UserListAPI.as_view()),
path("<int:id>/",UserDetailAPI.as_view()),
path("<int:id>/change-password/",UserChangePasswordAPI.as_view()),
path("forgot-password/",ForgotPasswordAPI.as_view()),
path("me/",UserProfileView.as_view()),
path("reset-password/",ResetPasswordAPI.as_view())
]