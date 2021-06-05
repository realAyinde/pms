from django.db import models
from ehr.models import BaseModel
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    NON_BINARY = 'N', _('Non Binary')
    OTHERS = 'O', _('I Prefer not to Say')

class BloodGroup(models.TextChoices):
    A_POSITIVE = 'A+', _('A+')
    B_POSITIVE = 'B+', _('B+')
    O_POSITIVE = 'O+', _('A+')
    A_NEGATIVE = 'A-', _('A-')
    B_NEGATIVE = 'B-', _('B-')
    O_NEGATIVE = 'O-', _('O-')

class Genotype(models.TextChoices):
    AA = 'AA', _('AA')
    AS = 'AS', _('AS')
    SS = 'SS', _('SS')
    SC = 'SC', _('SC')

class Doctor(BaseModel):
    title = models.CharField(max_length=20, null=True, default = 'Dr')
    description = models.CharField(max_length=20, null=True, default = 'Medical Doctor')
    name = models.CharField(max_length=200, default='Treat Me')
    phone_number = models.CharField(max_length=20, default="08108160545")
    license_number = models.IntegerField(null=True, default =1237890)
    specialty = models.CharField(max_length=200, default='Physician')
    hospital = models.CharField(max_length=200, default='Nairobi Hospital')
    profile_photo = models.ImageField(upload_to='doctor_profiles/', default='doctor_profiles/no-image.jpg')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class NextOfKin(BaseModel):
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, default="08108160545")
    email = models.EmailField()
    def __str__(self):
        return self.name

class Medicine(BaseModel):
    name = models.CharField(max_length=200)
    date_given = models.DateTimeField()
    doctor_prescribed = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class MedicalCover(BaseModel):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    type_of_cover = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class AllergiesAndDirectives(BaseModel):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Patient(BaseModel):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    occupation = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, default="08108160545")
    address = models.TextField()
    gender = models.CharField(max_length=6, choices=Gender.choices)
    status = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    registration_number = models.IntegerField(unique=True)
    blood_group = models.CharField(max_length=5, choices=BloodGroup.choices, null=True)
    next_of_kin = models.OneToOneField(NextOfKin, on_delete=models.CASCADE)
    medications = models.ForeignKey(Medicine, null=True, blank=True, on_delete=models.CASCADE)
    medical_cover = models.ForeignKey(MedicalCover, blank=True, null=True, on_delete=models.CASCADE)
    allergies_and_directives = models.ForeignKey(AllergiesAndDirectives, blank=True, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='patients_photo/', null=True)

    @classmethod
    def search_by_registration_number(cls, registration_number):
        patient = cls.objects.filter(registration_number__icontains=registration_number)
        return patient
        
class Treatment(BaseModel):
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    consultation_fee = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    recommendations = models.TextField(null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.patient.name + " @ " + self.date.strftime("%d-%b-%Y (%H:%M:%S %A)")
