from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from .models import *

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def index_view(request):
    return render(request,"users/index_page.html")

def home_view(request):
    return render(request,"users/home_page.html")

def profile_view(request):
    print("Logged in user:- ", request.user, request.user.id)
    logged_in_user_profile = Profile.objects.get(user=request.user)
    return render(request,"users/profile_page.html",{"profile":logged_in_user_profile})

def update_profile(request,pk):
    selectedProfile = Profile.objects.get(id=pk)
    if request.method=="POST":
        userEmail = request.POST["useremail"]
        userBio = request.POST["bio"]
        userInterest = request.POST["interests"]

        selectedProfile.user.email = userEmail
        selectedProfile.bio = userBio
        selectedProfile.interests = userInterest
        selectedProfile.save()
        selectedProfile.user.save()

        return redirect('profile')
    else:
        return redirect('profile')


def logout_view(request):
    logout(request)
    return redirect('login')