# Generated by Django 5.0.3 on 2024-03-12 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0007_alter_doctor_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="search",
            field=models.CharField(default="", max_length=1),
        ),
    ]
