from rest_framework.response import Response
from rest_framework.decorators import api_view
from database.models import User, Doctor
from .serializers import UserSerializer, DoctorSerializer


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
            doctor = Doctor.objects.get(crm=doctor_crm)
            serializer = DoctorSerializer(doctor)

            response = Response(serializer.data)
            if not doctor:
                response = Response({"message": "Doctor Not Found"}, status=404)

        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            response = Response(serializer.data)

        return response

    elif request.method == "POST":
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=201)
        else:
            response = Response(serializer.errors, status=400)
        return response

    elif request.method == "PUT" and doctor_crm is not None:
        try:
            response = Response({"message": "Internal Error"}, status=500)
            doctor = Doctor.objects.get(crm=doctor_crm)
            serializer = DoctorSerializer(doctor, data=request.data)

            if request.data is None:
                response = Response({"message": "Data is missing"}, status=400)
            elif not doctor:
                response({"message": "Doctor Not Found"}, status=404)
            elif serializer.is_valid():
                serializer.save()
                response = Response(serializer.data)
        except Exception as e:
            response = Response({"message": str(e)}, status=500)

        return response

    elif request.method == "DELETE" and doctor_crm is not None:
        response = Response({"message": "Internal Error"}, status=500)

        doctor = Doctor.objects.get(crm=doctor_crm)
        if not doctor:
            response({"message": "Doctor Not Found"}, status=404)

        doctor.delete()
        response = Response({"message": "Doctor Deleted"})

        return response
