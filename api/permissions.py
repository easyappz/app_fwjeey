from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """Permission class to check if user is authenticated"""
    
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'is_authenticated') and request.user.is_authenticated
