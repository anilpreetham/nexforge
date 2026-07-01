from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import (
    CustomUser,
    Role,
    UserRole,
)


from apps.authentication.services.jwt_service import JWTService
from apps.authentication.services.role_service import RoleService


class AuthenticationService:

    @staticmethod
    def register(validated_data):

        role_name = validated_data.pop("role")

        if CustomUser.objects.filter(
            username=validated_data["username"]
        ).exists():
            raise Exception("Username already exists.")

        if CustomUser.objects.filter(
            email=validated_data["email"]
        ).exists():
            raise Exception("Email already exists.")

        password = validated_data.pop("password")

        user = CustomUser(**validated_data)

        user.set_password(password)

        user.save()

        role = Role.objects.get(
            name=role_name
        )

        UserRole.objects.create(
            user=user,
            role=role
        )

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role.name,
        }

    @staticmethod
    def login(username, password):

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise Exception(
                "Invalid username or password."
            )

        tokens = JWTService.generate_tokens(user)

        roles = RoleService.get_roles(user)

        permissions = RoleService.get_permissions(user)

        dashboard = RoleService.get_dashboard(user)

        return {

            "access_token": tokens["access_token"],

            "refresh_token": tokens["refresh_token"],

            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },

            "roles": roles,

            "permissions": permissions,

            "dashboard": dashboard,

        }

    @staticmethod
    def logout(refresh_token):

        token = RefreshToken(refresh_token)

        token.blacklist()

        return {

            "message": "Logged out successfully."

        }

    @staticmethod
    def refresh(refresh_token):

        return JWTService.refresh_tokens(
            refresh_token
        )
