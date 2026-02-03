from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MembershipViewSet, MembershipRegistrationViewSet

router = DefaultRouter()
router.register(r'', MembershipViewSet, basename='membership')
router.register(r'registrations', MembershipRegistrationViewSet, basename='membership-registration')

urlpatterns = [
    path('', include(router.urls)),
]
