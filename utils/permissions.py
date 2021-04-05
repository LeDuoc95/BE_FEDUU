from rest_framework.permissions import BasePermission


class CustomBasePermission(BasePermission):
    message = 'You do not have permission to operate!!!'


class IsLecturerOrAdmin(CustomBasePermission):
    def has_permission(self, request, view):
        return bool(request.user.position == 0 or request.user.position == 1)


class IsAdmin(CustomBasePermission):
    def has_permission(self, request, view):
        return bool(request.user.position == 0)


class IsLecturer(CustomBasePermission):
    """
       Allows access only to authenticated users with user type is employee.
       """

    def has_permission(self, request, view):
        return bool(request.user.position == 1)


class IsStudy(CustomBasePermission):
    def has_permission(self, request, view):
        return bool(request.user.position == 2)
