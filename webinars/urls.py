from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebinarViewSet, WebinarRegistrationViewSet

router = DefaultRouter()
router.register(r'', WebinarViewSet, basename='webinar')
router.register(r'registrations', WebinarRegistrationViewSet, basename='webinar-registration')

urlpatterns = [
    path('', include(router.urls)),
]
