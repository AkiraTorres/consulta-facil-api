from rest_framework.exceptions import APIException


class InternalErrorException(APIException):
    status_code = 500
    default_detail = "Internal Error"
    default_code = "internal_error"


class UserNotFoundException(APIException):
    status_code = 404
    default_detail = "User Not Found"
    default_code = "user_not_found"


class DataMissingException(APIException):
    status_code = 400
    default_detail = "Missing data"
    default_code = "data_missing"


class DoctorNotFoundException(APIException):
    status_code = 404
    default_detail = "Doctor Not Found"
    default_code = "doctor_not_found"


class AdminNotFoundException(APIException):
    status_code = 404
    default_detail = "Admin Not Found"
    default_code = "admin_not_found"


class DoctorAvailabilityNotFoundException(APIException):
    status_code = 404
    default_detail = "Doctor Availability Not Found"
    default_code = "doctor_availability_not_found"


class AppointmentNotFoundException(APIException):
    status_code = 404
    default_detail = "Appointment Not Found"
    default_code = "appointment_not_found"
