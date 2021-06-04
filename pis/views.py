from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, NextOfKin, MedicalCover, AllergiesAndDirectives, Medicine, Treatment
from .forms import UpdateProfileForm, NewPatientForm, NewNextOfKinForm, NewMedicineForm, MedicalCoverForm, AllergiesAndDirectivesForm, TreatmentForm
from .email import send_medical_report_patient
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
# import Response from the rest_framework response module. This will handle the response from the API requests
from rest_framework.response import Response
# import APIView that will act as a base class for the API view function
from rest_framework.views import APIView
#import UserInformation class from the models
from .models import Doctor
#import UserInformationSerializer class from the serializer module
from .serializer import DoctorSerializer, PatientSerializer
# Create your views here.


@login_required(login_url='/accounts/login')
def dashboard(request):
    current_user = request.user
    doctor = Doctor.objects.get(user_id=current_user.id)
    return render(request, 'dashboard.html', {'doctor':doctor})

@login_required(login_url='/accounts/login')
def profile(request):
    current_user = request.user
    doctor = Doctor.objects.get(user_id=current_user.id)
    return render(request, 'profile.html', {'doctor':doctor})

@login_required(login_url='/accounts/login')
def update_profile(request, username):
    current_user = request.user
    username = current_user.username
    doctor = Doctor.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save()
        return redirect('myProfile')
    else:
        form = UpdateProfileForm()
    return render(request, 'update_profile.html', {'form':form, 'doctor':doctor})

@login_required(login_url='/accounts/login')
def messages(request):
    current_user = request.user
    doctor = Doctor.objects.get(user_id=current_user.id)

    return render(request, 'messages.html', {'doctor':doctor, 'patients':patients})

@login_required(login_url='/accounts/login')
def patients(request):
    current_user = request.user
    doctor = Doctor.objects.get(user_id=current_user.id)
    patients  = Patient.objects.all().filter(doctor=doctor)
    return render(request, 'patients.html', {'patients':patients, 'doctor':doctor})

def new_patient(request):
    current_user = request.user
    doctor = Doctor.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = NewPatientForm(request.POST, request.FILES)
        nform = NewNextOfKinForm(request.POST, request.FILES)
        mform = NewMedicineForm(request.POST, request.FILES)
        adform = AllergiesAndDirectivesForm(request.POST, request.FILES)
        if mform.is_valid() and nform.is_valid() and form.is_valid():
            next_of_kin = nform.save()
            next_of_kin.save()
            print("Go on soun")
        elif mform.is_valid():
            medicine = mform.save()
            medicine.doctor =doctor
            medicine.save()
            print("Go on soun")
        elif adform.is_valid():
            allergies = adform.save()
            allergies.save()
            print("Go on soun")
        if form.is_valid():
            patient = form.save()
            patient.doctor = doctor
            patient.save()
            # reg_no = form.cleaned_data.get("registration_number")
            # print(reg_no)
        return redirect('allPatients')

    # if request.method == 'POST':
    #     nform = NewNextOfKinForm(request.POST, request.FILES)
    #     if nform.is_valid():
    #         next_of_kin = nform.save()
    #         next_of_kin.save()
    #     return redirect('allPatients')
    else:
        form = NewPatientForm()
        nform = NewNextOfKinForm()
        mform = NewMedicineForm()
        mcform = MedicalCoverForm()
        adform = AllergiesAndDirectivesForm()
    return render(request, 'new_patient.html', {'doctor':doctor, 'form':form, 'nform':nform, 'mform':mform, 'mcform':mcform, 'adform':adform})

@login_required(login_url='/accounts/login')
def single_patient(request, registration_number):
    current_user = request.user
    patient = Patient.objects.get(registration_number = registration_number)
    next_of_kin = NextOfKin.objects.get_or_none(id=patient.next_of_kin_id)
    doctor = Doctor.objects.get(user_id=current_user.id)
    medical_cover = MedicalCover.objects.get_or_none(id=patient.medical_cover_id)
    allergies = AllergiesAndDirectives.objects.get_or_none(id = patient.allergies_and_directives_id)
    medicine = Medicine.objects.get_or_none(id=patient.medications_id)
    try:
        doctor_prescribing = Doctor.objects.get(id = medicine.doctor_prescribed_id)
    except:
        doctor_prescribing= None
        
    return render(request, 'single_patient.html', {'patient':patient, 'doctor':doctor, 'kin':next_of_kin, 'cover':medical_cover, 'allergies':allergies, 'medicine':medicine, 'doctor_prescribing':doctor_prescribing})

@login_required(login_url='/accounts/login')
def treatment(request, registration_number):
    current_user =request.user
    patient = Patient.objects.get(registration_number = registration_number)
    doctor = Doctor.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = TreatmentForm(request.POST, request.FILES)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.doctor = doctor
            treatment.patient = patient
            treatment.save()
    else:
        form = TreatmentForm()
    return render(request, 'treatment.html', {'patient':patient, 'doctor':doctor, 'form':form})

@login_required(login_url='/accounts/login')
def diagnosis(request, registration_number):
    current_user =request.user
    doctor = Doctor.objects.get(user_id=current_user.id)
    patient = Patient.objects.get(registration_number = registration_number)
    treatment = Treatment.objects.all().filter(patient_id=patient.id).first()
    name = patient.name
    email = patient.email
    send_medical_report_patient(name, email, treatment, doctor, patient)
    return render(request, 'diagnosis.html', {'doctor':doctor, 'patient':patient, 'treatment':treatment})

@login_required(login_url='/accounts/login')
def search_results(request):
    if 'registration_number' in request.GET and request.GET['registration_number']:
        current_user =request.user
        doctor = Doctor.objects.get(user_id=current_user.id)
        registration_number = request.GET.get('registration_number')
        try:
            patient = Patient.objects.get(registration_number=registration_number)
        except ObjectDoesNotExist:
            raise Http404()
        return render(request, 'search.html', {'patient':patient, 'doctor':doctor})

def handler404(request, exception):
    current_user = request.user
    doctor = Doctor.objects.get(user_id=current_user.id)
    return render(request, 'registration/404.html', {'doctor':doctor})

# Doctor List that inherits the APIView class from rest_framework library
class DoctorList(APIView):
    # get function to query database for all doctor objects
    def get(self, request, format = None):
        # query database to get all doctor objects.
        all_doctors = Doctor.objects.all()
        # convert all doctor objects to JSON objects
        serializers = DoctorSerializer(all_doctors, many = True)
        #return the JSON objects for when an get request is made
        return Response(serializers.data)

# Patient List that inherits the APIView class from rest_framework library
class PatientList(APIView):
    # get function to query database for all patient objects
    def get(self, request, format = None):
        # query database to get all patient objects.
        all_patients = Patient.objects.all()
        # convert all patient objects to JSON objects
        serializers = PatientSerializer(all_patients)
        #return the JSON objects for when an get request is made
        return Response(serializers.data)
