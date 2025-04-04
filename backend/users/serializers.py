from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User, City


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    city = serializers.IntegerField(
        required=False,
        validators=[UniqueValidator(queryset=City.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "gender",
            "age",
            "city",
        )
        extra_kwargs = {
            "username": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "gender": {"required": False},
            "age": {"required": False},
            "city": {"required": False},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data.get("username", None),
            first_name=validated_data.get("first_name", None),
            last_name=validated_data.get("last_name", None),
            gender=validated_data.get("gender", None),
            age=validated_data.get("age", None),
            city_id=validated_data.get("city", None),
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "password",
            "old_password",
        )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."}
            )

        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "gender",
            "age",
            "city",
        )
        extra_kwargs = {
            "username": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "gender": {"required": False},
            "age": {"required": False},
            "city": {"required": False},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value

    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."}
            )
        return value

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."}
            )

        instance.email = validated_data["email"]
        instance.username = validated_data.get("username", None)

        instance.first_name = validated_data.get("first_name", None)
        instance.last_name = validated_data.get("last_name", None)

        instance.gender = validated_data.get("gender", None)
        instance.age = validated_data.get("age", None)
        instance.city_id = validated_data.get("city", None)

        instance.save()

        return instance
