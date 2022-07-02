from rest_framework import permissions


class HasGroup(permissions.BasePermission):
    """
    Allows access only to specified group.
    """
    def __init__(self, group):
        super().__init__()
        self.group = group

    def has_permission(self, request, view):
        print(request.user)
        return bool(request.user.groups.filter(name=self.group))
