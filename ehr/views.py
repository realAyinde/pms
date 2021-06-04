from django.shortcuts import render

def forgotPassword(request):

    return render(request, 'registration/forgot_password.html')


