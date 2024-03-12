from rest_framework.response import Response
from rest_framework.decorators import api_view
from database.models import User, Doctor, Administrator, DoctorAvailability
from .serializers import *
from .exceptions import *
from .tools import *


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


@api_view(["GET"])
def validate_user(request, user_cpf=None):
    try:
        if user_cpf is None:
            raise DataMissingException()

        user = User.objects.get(cpf=user_cpf)
        if user:
            response = {"message": "User already exists.", "status": 400}
        else:
            response = {"message": "User don't exists.", "status": 200}

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
            else:
                raise DataMissingException()

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "PUT" and doctor_crm is not None:
        try:
            response = {"message": "Internal Error", "status": 500}
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


@api_view(["GET", "POST"])
def doctor_availability(request, doctor_crm=None, date=None):
    if request.method == "GET":
        if doctor_crm is not None and date is not None and date != "all":
            try:
                doctor_availability = DoctorAvailability.objects.filter(
                    doctor_crm=doctor_crm
                )
                if not doctor_availability:
                    raise DoctorAvailabilityNotFoundException()
                dates = []

                serializer = DoctorAvailabilitySerializer(
                    doctor_availability, many=True
                )

                for i in serializer.data:
                    # return Response(i)
                    if i.get("date")[0:10] == date[0:10]:
                        dates.append(i)

                response = Response(dates)

            except Exception as e:
                response = Response(
                    {"message": str(e)},
                    e.status_code if hasattr(e, "status_code") else 500,
                )

        elif doctor_crm is not None and date == "all":
            try:
                # return Response({"message": "all"})
                schedule = []

                doctor = Doctor.objects.get(crm=doctor_crm)
                if doctor is None:
                    raise DoctorNotFoundException()

                doctor_availability = DoctorAvailability.objects.filter(
                    doctor_crm=doctor
                )
                if not doctor_availability:
                    raise DoctorAvailabilityNotFoundException()

                serializer = DoctorAvailabilitySerializer(
                    doctor_availability, many=True
                )

                return Response(serializer.data)

                for i in serializer.data:
                    # print(i)
                    # break
                    time = select_time_by_date(serializer, i.date)
                    data = {"date": i.date, "times": time}
                    schedule.append(data)

                response = Response(schedule)

            except Exception as e:
                response = Response(
                    {"message": str(e)},
                    e.status_code if hasattr(e, "status_code") else 500,
                )

        else:
            doctor_availabilities = DoctorAvailability.objects.all()
            serializer = DoctorAvailabilitySerializer(doctor_availabilities, many=True)
            response = Response(serializer.data)

        return response

    elif request.method == "POST" and doctor_crm is not None:
        try:
            if request.data == {}:
                raise DataMissingException()

            doctor = Doctor.objects.get(crm=doctor_crm)
            if doctor is None:
                raise DoctorNotFoundException()

            converted = convert_date_to_db_format(request.data, doctor)

            DoctorAvailability.objects.bulk_create(converted)
            response = Response(request.data, status=201)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "PUT" and doctor_crm is not None:
        try:
            if request.data == {}:
                raise DataMissingException()

            alter_dates = []
            alter_dates.append([day.get("date") for day in request.data])

            doctor = Doctor.objects.get(crm=doctor_crm)
            if doctor is None:
                raise DoctorNotFoundException()

            doctor_availability = DoctorAvailability.objects.filter(
                doctor_crm=doctor_crm, date__in=alter_dates
            )
            # if not doctor_availability:
            #     raise DoctorAvailabilityNotFoundException()
            doctor_availability.delete()

            converted = convert_date_to_db_format(request.data, doctor)
            new_dates = DoctorAvailability.objects.bulk_create(converted)
            response = Response(new_dates, status=201)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "DELETE" and doctor_crm is not None:
        try:
            if doctor_crm is None:
                raise DataMissingException()

            doctor_availability = DoctorAvailability.objects.filter(
                doctor_crm=doctor_crm
            )
            if not doctor_availability:
                raise DoctorAvailabilityNotFoundException()

            doctor_availability.delete()
            response = Response({"message": "Doctor Availability Deleted"})

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )


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
