from rest_framework import permissions

class UpdateOwnUser(permissions.BasePermission):
    """Allow user to edit their own profile"""
    
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id

class PostOwnPurchase(permissions.BasePermission):
    """Allow user to make their own purchases"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to make their own purchase"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id.id == request.user.id