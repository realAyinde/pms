from .models import Patient, Doctor
from django.utils import timezone

now = timezone.now()

def total_patients_context_processor(request):
    current_user = request.user
    doctor = Doctor.objects.get(user_id=current_user.id)
    total_patients_counts = Patient.objects.filter(doctor=doctor).count()
    new_patients_counts = Patient.objects.filter(doctor=doctor, date_created__gte=now).count()
    visit_patients_counts = Patient.objects.filter(doctor=doctor, last_modified__gte=now).count()
    return {
        'total_patients_counts': total_patients_counts,
        'new_patients_counts': new_patients_counts,
        'visit_patients_counts':visit_patients_counts
    }