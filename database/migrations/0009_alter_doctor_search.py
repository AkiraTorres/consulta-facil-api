# Generated by Django 5.0.3 on 2024-03-12 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0008_doctor_search"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="search",
            field=models.CharField(max_length=1, null=True),
        ),
    ]
