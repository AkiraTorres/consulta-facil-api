# Generated by Django 5.0.3 on 2024-03-11 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0002_alter_user_data"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apointment",
            old_name="user_cpf",
            new_name="user_email",
        ),
        migrations.AlterField(
            model_name="user",
            name="birth_date",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
