from rest_framework import serializers

from apps.authentication.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser

        fields = [

            "id",

            "username",

            "email",

            "first_name",

            "last_name",

            "phone_number",

            "is_active"

        ]