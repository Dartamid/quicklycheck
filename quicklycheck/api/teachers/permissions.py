from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.teacher == request.user:
            return True
