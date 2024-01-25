from rest_framework.permissions import BasePermission
from .models import Project


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        field = "project_id"
        if not view.kwargs.get(field):
            field = "pk"
        try:
            project = Project.objects.get(pk=view.kwargs.get(field))
        except Project.DoesNotExist:
            return False
        return request.user == project.author_user_id


class IsProjectContributor(BasePermission):
    def has_permission(self, request, view):
        field = "project_id"
        if not view.kwargs.get(field):
            field = "pk"
        try:
            project = Project.objects.get(pk=view.kwargs.get(field))
        except Project.DoesNotExist:
            return False
        return request.user in project.contributors.all()


class PAuthorContributor(BasePermission):
    def has_permission(self, request, view):
        return IsProjectAuthor().has_permission(
            request, view
        ) or IsProjectContributor().has_permission(request, view)


class ProjectAuthorCreate(IsProjectAuthor):
    def has_permission(self, request, view):
        if view.action == "create":
            return super().has_permission(request, view)
        return True


class ProjectAuthorList(IsProjectAuthor):
    def has_permission(self, request, view):
        if view.action == "list":
            return super().has_permission(request, view)
        return True


class ProjectAuthorRetrieve(IsProjectAuthor):
    def has_permission(self, request, view):
        if view.action == "retrieve":
            return super().has_permission(request, view)
        return True


class ProjectAuthorUpdate(IsProjectAuthor):
    def has_permission(self, request, view):
        if view.action == "update":
            return super().has_permission(request, view)
        return True


class ProjectAuthorDelete(IsProjectAuthor):
    def has_permission(self, request, view):
        if view.action == "destroy":
            return super().has_permission(request, view)
        return True


class ProjectContributorCreate(IsProjectContributor):
    def has_permission(self, request, view):
        if view.action == "create":
            return super().has_permission(request, view)
        return True


class ProjectContributorList(IsProjectContributor):
    def has_permission(self, request, view):
        if view.action == "list":
            return super().has_permission(request, view)
        return True


class ProjectContributorRetrieve(IsProjectContributor):
    def has_permission(self, request, view):
        if view.action == "retrieve":
            return super().has_permission(request, view)
        return True


class ProjectContributorUpdate(IsProjectContributor):
    def has_permission(self, request, view):
        if view.action == "update":
            return super().has_permission(request, view)
        return True


class ProjectContributorDelete(IsProjectContributor):
    def has_permission(self, request, view):
        if view.action == "destroy":
            return super().has_permission(request, view)
        return True


class PAuthorContributorRetrieve(PAuthorContributor):
    def has_permission(self, request, view):
        if view.action == "retrieve":
            return super().has_permission(request, view)
        return True


class PAuthorContributorList(PAuthorContributor):
    def has_permission(self, request, view):
        if view.action == "list":
            return super().has_permission(request, view)
        return True
