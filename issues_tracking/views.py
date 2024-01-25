from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorWriteOnly, IsAuthorContributorReadOnly
from .serializers import ProjectSerializer, ProjectListSerializer
from .models import Project


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    list_serializer_class = ProjectListSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthorWriteOnly,
        IsAuthorContributorReadOnly,
    ]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        if self.action == "list":
            user = self.request.user
            return Project.objects.filter(Q(author_user_id=user) | Q(contributors=user))
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()


# class ContributorsViewset(ModelViewSet):
#     serializer_class = ContributorSerializer
#     permission_classes = [IsAuthorWriteOnly, IsAuthorContributorReadOnly]
#     http_method_names = ["get", "post", "delete"]


# class IssuesViewset(ModelViewSet):
#     serializer_class = IssueSerializer
#     permission_classes = [IsContributorIssue]
#     http_method_names = ["get", "post", "put", "delete"]

#     def get_queryset(self):
#         return Issue.objects.filter(project__id=self.kwargs.get("project_id"))

#     def perform_create(self, serializer):
#         project = Project.objects.get(id=self.kwargs.get("project_id"))
#         serializer.save(author_user_id=self.request.user, project=project)


# class CommentsViewset(ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = [IsContributorComment]
#     http_method_names = ["get", "post", "put", "delete"]

#     def get_queryset(self):
#         return Comment.objects.filter(issue=self.kwargs.get("issue_id"))

#     def perform_create(self, serializer):
#         get_object_or_404(Project, id=self.kwargs.get("project_id"))
#         issue = get_object_or_404(Issue, id=self.kwargs.get("issue_id"))
#         serializer.save(author_user_id=self.request.user, issue=issue)
