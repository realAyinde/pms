from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import UserCreationForm
from users.forms import SignUpForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print("Saved Successfull!")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
        else:
            print("Unsuccessfull!")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def signOut(request):
    logout(request)

    return render(request, 'registration/logout.html')