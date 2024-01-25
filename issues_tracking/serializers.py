from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


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


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project", "permission", "role"]
        read_only_fields = ["project"]

    def validate(self, data):
        project_id = self.context["view"].kwargs.get("project_id")
        if not Project.objects.filter(id=project_id).exists():
            raise serializers.ValidationError("This project does not exist")
        user_id = data["user"].id
        if Contributor.objects.filter(project_id=project_id, user_id=user_id).exists():
            raise serializers.ValidationError(
                "This contributor already exists in this project"
            )
        return data

    def create(self, validated_data):
        project_id = self.context["view"].kwargs.get("project_id")
        validated_data["project_id"] = int(project_id)
        return super().create(validated_data)


class ContributorListSerializer(serializers.ModelSerializer):
    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ["user", "user_first_name", "user_last_name", "permission", "role"]

    def get_user_first_name(self, obj):
        return obj.user.first_name

    def get_user_last_name(self, obj):
        return obj.user.last_name


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "assignee_user_id",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "issue"]
        read_only_fields = ["issue"]
