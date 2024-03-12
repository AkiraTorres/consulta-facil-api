from rest_framework import serializers
from database.models import User, Doctor, Administrator, Apointment, DoctorAvailability


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = "__all__"


class DoctorAvailabilityByDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ["date"]


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = "__all__"
