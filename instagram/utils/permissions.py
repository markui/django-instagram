from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # check permissions for read-only request
            return True
        # check permissions for write request
        return obj.author == request.user
