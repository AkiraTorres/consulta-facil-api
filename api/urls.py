from django.urls import path
from . import views

urlpatterns = [
    path("user", views.user),
    path("user/<str:user_email>", views.user),
    path("doctor", views.doctor),
    path("doctor/<str:doctor_crm>", views.doctor),
    path("adm", views.admin),
    path("adm/<str:admin_email>", views.admin),
    path("user/validate/<str:user_cpf>", views.validate_user),
    path("doctor/availability/<str:doctor_crm>/<str:date>", views.doctor_availability),
    path("specialties", views.get_all_specialties),
    path("specialist/<str:specialty>", views.get_all_specialists_by_specialty),
    path("specialist/available/<str:doctor_crm>", views.get_available_days_by_doctor),
    path(
        "specialist/available/<str:doctor_crm>/<str:date>",
        views.get_available_times_by_doctor,
    ),
    path("appointment", views.appointment),
    path("appointment/user/<str:user_email>", views.get_appointments_by_user_email),
    path("appointment/doctor/<str:doctor_crm>", views.get_appointments_by_doctor_crm),
    path(
        "specialist/unavailable/<str:doctor_crm>/<str:date>",
        views.mark_doctor_availability_as_unavailable,
    ),
    path(
        "specialist/make_available/<str:doctor_crm>/<str:date>",
        views.mark_doctor_availability_as_unavailable,
    ),
    path("appointment/<int:id>", views.appointment),
    path(
        "appointment/doctor/<str:doctor_crm>/<str:date>",
        views.get_appointments_by_crm_and_date,
    ),
    path("doctor/email/<str:doctor_email>", views.get_doctor_by_email),
]
