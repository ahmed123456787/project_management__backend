from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError  # Correct import for ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Use the result of get_user_model(), not the function itself
        fields = ["name", "email", "password"]
        extra_kwargs = {  # Correct way to make fields write-only
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        """Validate the data"""
        if len(attrs.get("password", "")) < 5:  # Use .get() to avoid KeyError
            raise ValidationError({"password": "The password must be above 5 characters."})
        return attrs

    def create(self, validated_data):
        """Create a new user with encrypted password"""
        user_model = get_user_model()
        return user_model.objects.create_user(**validated_data)
