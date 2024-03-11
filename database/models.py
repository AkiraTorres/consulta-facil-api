from django.db import models

# Create your models here.


class User(models.Model):
    cpf = models.CharField(max_length=11, null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(primary_key=True)
    address = models.CharField(max_length=100, null=True)
    neighborhood = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=2, null=True)
    house_number = models.CharField(max_length=5, null=True)
    cep = models.CharField(max_length=8, null=True)
    birth_date = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=25)
    phone = models.CharField(max_length=11, null=True)
    data = models.BooleanField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Doctor(models.Model):
    crm = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    specialist = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    user_type = models.CharField(max_length=25)
    gender = models.CharField(max_length=5)
    description = models.TextField()
    token = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Administrator(models.Model):
    email = models.EmailField(primary_key=True)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Apointment(models.Model):
    id = models.AutoField(primary_key=True)
    user_email = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_crm = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25)
