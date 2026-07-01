from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.serializers import (
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
    RegisterSerializer,
    RefreshTokenSerializer,
)

from apps.authentication.services import AuthenticationService


class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthenticationService.register(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "User registered successfully.",
                "data": user,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = AuthenticationService.login(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "success": True,
                "message": "Login Successful",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthenticationService.logout(
            serializer.validated_data["refresh"]
        )

        return Response(
            {
                "success": True,
                "message": "Logout successful",
            },
            status=status.HTTP_200_OK,
        )


class RefreshAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = AuthenticationService.refresh(
            serializer.validated_data["refresh"]
        )

        return Response(
            {
                "success": True,
                "message": "Token refreshed successfully.",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )