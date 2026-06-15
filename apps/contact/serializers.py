# apps/contact/serializers.py
from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    # Honeypot: hidden from real users, bots tend to fill it. Must stay empty.
    website = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )

    class Meta:
        model = Contact
        fields = ["id", "name", "email", "message", "website", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_website(self, value):
        if value:
            raise serializers.ValidationError("Spam detected.")
        return value

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Please enter your name.")
        return value

    def validate_message(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters."
            )
        if len(value) > 5000:
            raise serializers.ValidationError("Message is too long.")
        return value

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)
