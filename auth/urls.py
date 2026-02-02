from django.urls import path
from .views import UserChangePasswordAPI, ForgotPasswordAPI, ResetPasswordAPI,UserRegisterAPI
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("<int:id>/change-password/", UserChangePasswordAPI.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordAPI.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordAPI.as_view(), name="reset-password"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("register/",UserRegisterAPI.as_view(),name="register")
]