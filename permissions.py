from rest_framework import permissions


class HasGroup(permissions.BasePermission):
    """
    Allows access only to specified group.
    """
    def __init__(self, group):
        super().__init__()
        self.group = group

    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name=self.group))


class DeletePermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_superuser or request.user.groups.filter(name='dos')
        return True
