from rest_framework.response import Response
from rest_framework.decorators import api_view
from database.models import User, Doctor, Administrator
from .serializers import UserSerializer, DoctorSerializer, AdminSerializer
from .exceptions import *


@api_view(["GET", "POST", "PUT", "DELETE"])
def user(request, user_email=None):
    if request.method == "GET":
        if user_email is not None:
            try:
                user = User.objects.get(email=user_email)

                if not user:
                    raise UserNotFoundException()

                serializer = UserSerializer(user)
                response = Response(serializer.data)

            except Exception as e:
                response = Response(
                    {"message": str(e)},
                    e.status_code if hasattr(e, "status_code") else 500,
                )

        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            response = Response(serializer.data)

        return response

    elif request.method == "POST":
        try:
            if request.data == {}:
                raise DataMissingException()

            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data, status=201)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "PUT" and user_email is not None:
        try:
            if user_email is None:
                raise DataMissingException()

            user = User.objects.get(email=user_email)
            serializer = UserSerializer(user, data=request.data)

            if request.data == {}:
                raise DataMissingException()
            elif not user:
                raise UserNotFoundException()
            elif serializer.is_valid():
                serializer.save()
                response = Response(serializer.data)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "DELETE" and user_email is not None:
        try:
            if user_email is None:
                raise DataMissingException()

            user = User.objects.get(email=user_email)
            if not user:
                raise UserNotFoundException()

            user.delete()
            response = Response({"message": "User Deleted"})

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

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
            if request.data == {}:
                raise DataMissingException()

            serializer = DoctorSerializer(data=request.data)

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


@api_view(["GET", "POST", "PUT", "DELETE"])
def admin(request, admin_email=None):
    if request.method == "GET":
        if admin_email is not None:
            try:
                admin = Administrator.objects.get(email=admin_email)

                if not admin:
                    raise AdminNotFoundException()

                serializer = AdminSerializer(admin)
                response = Response(serializer.data)

            except Exception as e:
                response = Response(
                    {"message": str(e)},
                    e.status_code if hasattr(e, "status_code") else 500,
                )

        else:
            admins = Administrator.objects.all()
            serializer = AdminSerializer(admins, many=True)
            response = Response(serializer.data)

        return response

    elif request.method == "POST":
        try:
            if request.data == {}:
                raise DataMissingException()

            serializer = AdminSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data, status=201)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "PUT" and admin_email is not None:
        try:
            if admin_email is None:
                raise DataMissingException()

            admin = Administrator.objects.get(email=admin_email)
            serializer = AdminSerializer(admin, data=request.data)

            if request.data == {}:
                raise DataMissingException()
            elif not admin:
                raise AdminNotFoundException()
            elif serializer.is_valid():
                serializer.save()
                response = Response(serializer.data)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "DELETE" and admin_email is not None:
        try:
            if admin_email is None:
                raise DataMissingException()

            admin = Administrator.objects.get(email=admin_email)
            if not admin:
                raise AdminNotFoundException()

            admin.delete()
            response = Response({"message": "Admin Deleted"})

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response
