from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Lesson 07: anyone may READ an article; only its author may CHANGE or DELETE it."""

    message = "You can only change your own articles."

    def has_object_permission(self, request, view, obj):
        # GET, HEAD and OPTIONS are "safe" methods: they never change data.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Lesson 07: anyone may READ; only staff users may create, change or delete."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
