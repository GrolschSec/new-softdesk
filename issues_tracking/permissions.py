from rest_framework.permissions import BasePermission


class IsAuthorWriteOnly(BasePermission):
    """
    Permission check for authors of an object.
    Only authors or admins are allowed to update or delete the object.
    """

    def has_object_permission(self, request, view, obj):
        if view.action in ["update", "destroy"]:
            return request.user == obj.author_user_id
        return True


class IsAuthorContributorReadOnly(BasePermission):
    """
    Permission check for authors of an object.
    Only authors or admins are allowed to update or delete the object.
    """

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return (
                obj.contributors.filter(id=request.user.id).exists()
                or obj.author_user_id == request.user
            )
        return True
