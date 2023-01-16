from rest_framework.permissions import SAFE_METHODS, BasePermission


class APIPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user.is_superuser:
                return True

            if request.user.is_staff:
                return True

            return False
