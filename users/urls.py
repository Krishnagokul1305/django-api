from django.urls import path
from .views import UserListAPI,UserDetailAPI,UserProfileView

urlpatterns=[
path("",UserListAPI.as_view()),
path("<int:id>/",UserDetailAPI.as_view()),
path("me/",UserProfileView.as_view()),
]