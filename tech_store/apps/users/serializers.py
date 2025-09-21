from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from tech_store.apps.users.models import Customer, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm", "first_name", "second_name", "phone_number")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs["user"] = user
            return attrs

        raise serializers.ValidationError('Must include "email" and "password"')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "second_name",
            "phone_number",
            "role",
            "is_active",
            "date_joined",
            "updated_at",
        )
        read_only_fields = ("id", "date_joined", "updated_at")


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for customer profile.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ("id", "user", "date_of_birth")
        read_only_fields = ("id",)


class CustomerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating customer profile.
    """

    class Meta:
        model = Customer
        fields = ("date_of_birth",)

    def create(self, validated_data):
        user = self.context["request"].user
        customer, created = Customer.objects.get_or_create(user=user, defaults=validated_data)
        return customer
