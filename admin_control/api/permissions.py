from rest_framework.permissions import BasePermission


class IsAuthAdmin(BasePermission):
    
    """
    Allows access only to authenticated admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.user_role == 'ADMIN')
            
    