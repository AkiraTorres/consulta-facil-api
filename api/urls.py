from django.urls import path
from . import views

urlpatterns = [
    path("user", views.user),
    path("user/<str:user_cpf>", views.user),
    path("doctor", views.doctor),
    path("doctor/<str:doctor_crm>", views.doctor),
]
