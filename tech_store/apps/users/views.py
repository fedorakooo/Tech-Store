from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh_token = RefreshToken.for_user(user)

        return Response(
            data={
                "user": UserSerializer(user).data,
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        login(request, user)
        refresh_token = RefreshToken.for_user(user)

        return Response(
            data={
                "user": UserSerializer(user).data,
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
                "message": "User login successfully",
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(
            data={
                "message": "Logout successful",
            },
            status=status.HTTP_200_OK,
        )
    except Exception:
        return Response(
            data={
                "error": "Invalid token",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
