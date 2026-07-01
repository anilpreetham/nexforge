"""DRF serializers for enquiries."""

from rest_framework import serializers

from .models import Enquiry


class EnquirySerializer(serializers.ModelSerializer):
    """Public create + staff read/update. ``status``/``assigned_to`` are
    read-only on public create and only settable by authenticated staff."""

    class Meta:
        model = Enquiry
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "message",
            "enquiry_type",
            "status",
            "assigned_to",
            "created_at",
        ]
        read_only_fields = ["id", "assigned_to", "created_at"]

    def validate_message(self, value: str) -> str:
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Message is too short.")
        return value
