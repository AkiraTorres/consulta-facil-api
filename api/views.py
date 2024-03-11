from rest_framework.response import Response
from rest_framework.decorators import api_view
from database.models import User, Doctor
from .serializers import UserSerializer, DoctorSerializer
from .exceptions import *


@api_view(["GET", "POST", "PUT", "DELETE"])
def user(request, user_cpf=None):
    if request.method == "GET":
        if user_cpf is not None:
            user = User.objects.get(cpf=user_cpf)
            serializer = UserSerializer(user)

            response = Response(serializer.data)
            if not user:
                response = Response({"message": "User Not Found"}, status=404)

        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            response = Response(serializer.data)

        return response

    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=201)
        else:
            response = Response(serializer.errors, status=400)
        return response

    elif request.method == "PUT" and user_cpf is not None:
        response = Response({"message": "Internal Error"}, status=500)
        serializer = UserSerializer(user, data=request.data)
        user = User.objects.get(cpf=user_cpf)

        if request.data is None:
            response = Response({"message": "Data is missing"}, status=400)
        elif not user:
            response({"message": "User Not Found"}, status=404)
        elif serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)

        return response

    elif request.method == "DELETE" and user_cpf is not None:
        response = Response({"message": "Internal Error"}, status=500)

        user = User.objects.get(cpf=user_cpf)
        if not user:
            response({"message": "User Not Found"}, status=404)

        user.delete()
        response = Response({"message": "User Deleted"})

        return response


@api_view(["GET", "POST", "PUT", "DELETE"])
def doctor(request, doctor_crm=None):
    if request.method == "GET":
        if doctor_crm is not None:
            try:
                doctor = Doctor.objects.get(crm=doctor_crm)
                if not doctor:
                    raise DoctorNotFoundException()

                serializer = DoctorSerializer(doctor)
                response = Response(serializer.data)

            except Exception as e:
                response = Response(
                    {"message": str(e)},
                    e.status_code if hasattr(e, "status_code") else 500,
                )

        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            response = Response(serializer.data)

        return response

    elif request.method == "POST":
        try:
            serializer = DoctorSerializer(data=request.data)

            if request.data == {}:
                raise DataMissingException()

            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data, status=201)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "PUT" and doctor_crm is not None:
        try:
            if doctor_crm is None:
                raise DataMissingException()

            doctor = Doctor.objects.get(crm=doctor_crm)
            serializer = DoctorSerializer(doctor, data=request.data)

            if request.data == {}:
                raise DataMissingException()
            elif not doctor:
                raise DoctorNotFoundException()
            elif serializer.is_valid():
                serializer.save()
                response = Response(serializer.data)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "DELETE" and doctor_crm is not None:
        try:
            if doctor_crm is None:
                raise DataMissingException()

            doctor = Doctor.objects.get(crm=doctor_crm)
            if not doctor:
                raise DoctorNotFoundException()

            doctor.delete()
            response = Response({"message": "Doctor Deleted"})

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response
