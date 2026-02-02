from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsStaffOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.id==obj.id