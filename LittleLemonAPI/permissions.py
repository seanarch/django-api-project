# permissions.py
from rest_framework.permissions import BasePermission

class CanManageMenuItemPermission(BasePermission):
    def has_permission(self, request, view):
        # Allow GET requests to all authenticated users
        if request.method == 'GET':
            return True
        # Allow POST requests only for users in the "manager" group
        if request.method == 'POST' and request.user.groups.filter(name='manager').exists():
            return True
        # Deny PUT, PATCH, and DELETE for all users
        return False
