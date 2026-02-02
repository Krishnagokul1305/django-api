from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InternshipViewSet

router = DefaultRouter()
router.register(r'', InternshipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
