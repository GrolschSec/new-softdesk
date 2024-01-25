from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    ProjectAuthorCreate,
    ProjectAuthorUpdate,
    ProjectAuthorDelete,
    PAuthorContributorRetrieve,
    PAuthorContributorList,
)
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    ContributorSerializer,
    ContributorListSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .models import Project, Contributor, Comment, Issue


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    list_serializer_class = ProjectListSerializer
    permission_classes = [
        IsAuthenticated,
        ProjectAuthorUpdate,
        ProjectAuthorDelete,
        PAuthorContributorRetrieve,
    ]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        if self.action == "list":
            user = self.request.user
            return Project.objects.filter(
                Q(author_user_id=user) | Q(contributors=user)
            ).order_by("id")
        return Project.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()


class ContributorsViewset(ModelViewSet):
    list_serializer_class = ContributorListSerializer
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    http_method_names = ["get", "post", "delete"]
    permission_classes = [
        IsAuthenticated,
        ProjectAuthorCreate,
        ProjectAuthorDelete,
        PAuthorContributorList,
    ]

    def get_queryset(self):
        return Contributor.objects.filter(
            project=self.kwargs.get("project_id")
        ).order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()

    def get_object(self):
        if self.action == "destroy":
            return get_object_or_404(
                self.get_queryset(),
                user=self.kwargs.get("pk"),
            )
        return super().get_object()


class IssuesViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Issue.objects.filter(project__id=self.kwargs.get("project_id"))

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs.get("project_id"))
        serializer.save(author_user_id=self.request.user, project=project)


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs.get("issue_id"))

    def perform_create(self, serializer):
        get_object_or_404(Project, id=self.kwargs.get("project_id"))
        issue = get_object_or_404(Issue, id=self.kwargs.get("issue_id"))
        serializer.save(author_user_id=self.request.user, issue=issue)
