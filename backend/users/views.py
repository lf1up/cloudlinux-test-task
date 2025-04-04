from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from users.serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
)
from users.permissions import IsActive


class RegisterView(generics.CreateAPIView):
    """
    View to register a new user.
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    View to change user password.
    """

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    """
    View to update user profile.
    """

    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsActive,
    )
    serializer_class = UpdateUserSerializer


class GetTokenPairView(APIView):
    """
    View to get token pair for user.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data.get("email", None)
            username = request.data.get("username", None)
            password = request.data["password"]

            if username is None and email is None:
                return Response(
                    {
                        "username": [_("This field is required.")],
                        "email": [_("This field is required.")],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = None
            if email is not None:
                user = User.objects.get(email=email)
            elif username is not None:
                user = User.objects.get(username=username)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user_id": user.id,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"password": [_("Unable to log in with provided credentials.")]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    """
    View to logout user.
    """

    permission_classes = (
        IsAuthenticated,
        IsActive,
    )

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "OK"}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"message": "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST
            )
