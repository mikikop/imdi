from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, UpdateForm
from django.contrib.auth.models import User
from cprint import cprint
from django.contrib import messages



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = LoginForm()
    print(dir(request))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request,'Log in failed')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def profile(request):
    return render(request, 'profile.html')

# def profile(request, id):
#     user = User.objects.get(pk=id)
#     return render(request, 'profile.html', {'user': user})

def edit_profile(request):
    form = UpdateForm(instance = request.user)
    if request.method == 'POST':
        form = UpdateForm(request.POST,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'The update succeeded')
            return redirect ('edit_profile')
        else:
            messages.error(request,'The update failed')
            return render(request, 'edit_profile.html', {'form': form})
    return render(request, 'edit_profile.html', {'form': form})
