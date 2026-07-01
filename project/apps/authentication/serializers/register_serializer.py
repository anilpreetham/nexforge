from rest_framework import serializers

from apps.authentication.models import CustomUser, Role


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    role = serializers.ChoiceField(
        choices=[]
    )

    class Meta:
        model = CustomUser

        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].choices = [
            (role.name, role.name)
            for role in Role.objects.all()
        ]