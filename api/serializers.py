from rest_framework import serializers
from database.models import User, Doctor, Administrator, Apointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = "__all__"
