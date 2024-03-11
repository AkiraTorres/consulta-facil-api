from rest_framework import serializers
from database.models import User, Doctor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        # extra_kwargs = {"__all__": {"required": False}}
