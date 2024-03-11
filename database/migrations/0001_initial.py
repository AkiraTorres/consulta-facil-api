# Generated by Django 5.0.3 on 2024-03-11 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Administrator",
            fields=[
                (
                    "email",
                    models.EmailField(
                        max_length=254, primary_key=True, serialize=False
                    ),
                ),
                ("token", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "crm",
                    models.CharField(max_length=11, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
                ("specialist", models.CharField(max_length=100)),
                ("specialty", models.CharField(max_length=100)),
                ("user_type", models.CharField(max_length=25)),
                ("gender", models.CharField(max_length=5)),
                ("description", models.TextField()),
                ("token", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=11)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("cpf", models.CharField(max_length=11, null=True)),
                ("name", models.CharField(max_length=100, null=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, primary_key=True, serialize=False
                    ),
                ),
                ("address", models.CharField(max_length=100, null=True)),
                ("neighborhood", models.CharField(max_length=100, null=True)),
                ("city", models.CharField(max_length=100, null=True)),
                ("state", models.CharField(max_length=2, null=True)),
                ("house_number", models.CharField(max_length=5, null=True)),
                ("cep", models.CharField(max_length=8, null=True)),
                ("birth_date", models.DateTimeField(null=True)),
                ("user_type", models.CharField(max_length=25)),
                ("phone", models.CharField(max_length=11, null=True)),
                ("data", models.TextField()),
                ("token", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Apointment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(max_length=25)),
                (
                    "doctor_crm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="database.doctor",
                    ),
                ),
                (
                    "user_cpf",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="database.user"
                    ),
                ),
            ],
        ),
    ]
