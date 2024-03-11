from django.urls import path
from . import views

urlpatterns = [
    path("user", views.user),
    path("user/<str:user_email>", views.user),
    path("doctor", views.doctor),
    path("doctor/<str:doctor_crm>", views.doctor),
    path("admin", views.admin),
    path("admin/<str:admin_email>", views.admin),
]
