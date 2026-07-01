from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Validates login request.
    """

    username = serializers.CharField(
        max_length=150,
        required=True
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )