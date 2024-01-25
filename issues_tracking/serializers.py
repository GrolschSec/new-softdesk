from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Project  # , Contributor  # , Issue, Comment,


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author_user_id"]
        read_only_fields = ["author_user_id"]

    def create(self, validated_data):
        validated_data["author_user_id"] = self.context["request"].user
        return super().create(validated_data)


# class ContributorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contributor
#         fields = ["user", "project", "permission", "role"]

#     def create(self):
#         project_id = self.context["view"].kwargs.get("project_id")
#         project = Project.objects.get(id=project_id)
#         self.validated_data["project"] = project
#         return super().create(self.validated_data)

# class IssueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Issue
#         fields = [
#             "id",
#             "title",
#             "description",
#             "tag",
#             "priority",
#             "status",
#             "assignee_user_id",
#         ]


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ["id", "description", "issue"]
#         read_only_fields = ["issue"]
