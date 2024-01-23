from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "password"]

    def validate_email(self, value):
        model = self.Meta.model
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        if model.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise exceptions.AuthenticationFailed("Invalid email/password")
        attrs["access"] = str(RefreshToken.for_user(user).access_token)
        del attrs["email"]
        del attrs["password"]
        return attrs
