from rest_framework.response import Response
from rest_framework.decorators import api_view
from database.models import *
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

            for d in converted:
                d.save()

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


@api_view(["GET"])
def get_all_specialties(request):
    try:
        specialties = Doctor.objects.values("specialty").distinct()
        response = Response(specialties)

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET"])
def get_all_specialists_by_specialty(request, specialty=None):
    try:
        if specialty is None:
            raise DataMissingException()

        specialists = Doctor.objects.filter(specialty=specialty)
        if not specialists:
            raise DoctorNotFoundException()

        serializer = DoctorSerializer(specialists, many=True)
        response = Response(serializer.data)

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET"])
def get_available_days_by_doctor(request, doctor_crm=None):
    if request.method == "GET":
        try:
            if doctor_crm is None:
                raise DataMissingException()

            doctor = Doctor.objects.get(crm=doctor_crm)
            if doctor is None:
                raise DoctorNotFoundException()

            doctor_availability = DoctorAvailability.objects.filter(
                doctor_crm=doctor, available=True
            )
            if not doctor_availability:
                raise DoctorAvailabilityNotFoundException()

            days = []
            for day in doctor_availability:
                days.append(day.date[0:10])
            unique_days = list(set(days))

            # serializer = DoctorAvailabilityByDateSerializer(doctor_availability, many=True)
            response = Response(unique_days)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response


@api_view(["GET"])
def get_available_times_by_doctor(request, doctor_crm=None, date=None):
    try:
        if doctor_crm is None or date is None:
            raise DataMissingException()

        doctor = Doctor.objects.get(crm=doctor_crm)
        if doctor is None:
            raise DoctorNotFoundException()

        doctor_availability = DoctorAvailability.objects.filter(
            doctor_crm=doctor, date__startswith=date, available=True
        )
        if not doctor_availability:
            raise DoctorAvailabilityNotFoundException()

        serializer = DoctorAvailabilitySerializer(doctor_availability, many=True)

        times = select_time_by_date(serializer, date)
        response = Response(times)

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET", "POST", "PUT", "DELETE"])
def appointment(request, id=None):
    if request.method == "GET":
        if id is not None:
            try:
                consult = Appointment.objects.get(id=id)
                if not consult:
                    raise AppointmentNotFoundException()

                serializer = AppointmentSerializer(consult)
                response = Response(serializer.data)

            except Exception as e:
                response = Response(
                    {"message": str(e)},
                    e.status_code if hasattr(e, "status_code") else 500,
                )

        else:
            appointments = Appointment.objects.all()
            serializer = AppointmentSerializer(appointments, many=True)
            response = Response(serializer.data)

        return response

    elif request.method == "POST":
        try:
            if request.data == {}:
                raise DataMissingException()

            serializer = AppointmentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data, status=201)

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response

    elif request.method == "DELETE":
        try:
            consult = Appointment.objects.get(id=id)
            if not consult:
                raise AppointmentNotFoundException()

            consult.delete()
            response = Response({"message": "Appointment Deleted"})

        except Exception as e:
            response = Response(
                {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
            )

        return response


@api_view(["GET"])
def get_appointments_by_user_email(request, user_email):
    try:
        consult = Appointment.objects.filter(user_email=user_email)
        if not consult:
            raise AppointmentNotFoundException()

        serializer = AppointmentSerializer(consult, many=True)
        response = Response(serializer.data)

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET"])
def get_appointments_by_doctor_crm(request, doctor_crm):
    try:
        consult = Appointment.objects.filter(doctor_crm=doctor_crm)
        if not consult:
            raise AppointmentNotFoundException()

        serializer = AppointmentSerializer(consult, many=True)
        response = Response(serializer.data)

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET"])
def get_appointments_by_crm_and_date(request, doctor_crm, date):
    try:
        consult = Appointment.objects.filter(
            doctor_crm=doctor_crm, date__startswith=date
        )
        if not consult:
            raise AppointmentNotFoundException()

        serializer = AppointmentSerializer(consult, many=True)
        response = Response(serializer.data)

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET"])
def mark_doctor_availability_as_unavailable(request, doctor_crm, date):
    try:
        doctor = Doctor.objects.get(crm=doctor_crm)
        if doctor is None:
            raise DoctorNotFoundException()

        doctor_availability = DoctorAvailability.objects.filter(
            doctor_crm=doctor, date__startswith=date
        )
        if not doctor_availability:
            raise DoctorAvailabilityNotFoundException()

        for d in doctor_availability:
            d.available = False
            d.save()

        response = Response({"message": "Doctor Availability Updated"})

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET"])
def mark_doctor_availability_as_unavailable(request, doctor_crm, date):
    try:
        doctor = Doctor.objects.get(crm=doctor_crm)
        if doctor is None:
            raise DoctorNotFoundException()

        doctor_availability = DoctorAvailability.objects.filter(
            doctor_crm=doctor, date__startswith=date
        )
        if not doctor_availability:
            raise DoctorAvailabilityNotFoundException()

        for d in doctor_availability:
            d.available = True
            d.save()

        response = Response({"message": "Doctor Availability Updated"})

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response


@api_view(["GET"])
def get_doctor_by_email(request, doctor_email):
    try:
        doctor = Doctor.objects.get(email=doctor_email)
        if doctor is None:
            raise DoctorNotFoundException()

        serializer = DoctorSerializer(doctor)
        response = Response(serializer.data)

    except Exception as e:
        response = Response(
            {"message": str(e)}, e.status_code if hasattr(e, "status_code") else 500
        )

    return response
