from database.models import DoctorAvailability
from .serializers import DoctorAvailability, DoctorAvailabilityByDateSerializer


def select_time_by_date(serializer, given_date):
    dates = []
    for i in serializer.data:
        if i.date[0:9] == given_date[0:9]:
            dates.append(i)

    return dates


def convert_date_to_db_format(schedule, doctor):
    all = []

    for day in schedule:
        for available_time in day.get("available_times"):
            all.append(
                DoctorAvailability(
                    doctor_crm=doctor, date=f"{day.get("date")} {available_time}", available=True
                )
            )
    return all

def convert_day_to_db_format(schedule, doctor):
    all = []
    
    for available_time in schedule.get("available_times"):
        all.append(
            DoctorAvailability(
                doctor_crm=doctor, date=f"{schedule.get("date")} {available_time}", available=True
            )
        )
    return all
