from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InternshipViewSet, InternshipRegistrationViewSet

router = DefaultRouter()
router.register(r'list', InternshipViewSet, basename='internship')
router.register(r'registrations', InternshipRegistrationViewSet, basename='internship-registration')

urlpatterns = [
    path('', include(router.urls)),
]