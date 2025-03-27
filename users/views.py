from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from .models import *
from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("Inside the valide form")
            user = form.save()
            # create the profile instance
            Profile.objects.create(
                user = user,
                bio = form.cleaned_data['bio'],
                interests = form.cleaned_data['interests']
            )
            print('Returning')
            messages.success(request,"Register successful!,Please login into your accont.")
            return redirect('login')
        else:
            print("Inside else :- form is not valid")
            print(form.errors)
            for field, errors in form.errors.items():
                print(errors)
            return render(request,'users/register.html',{"form":form})
    else:
        print('Inside the else')
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Login successful!')
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login')
        
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

        messages.success(request,"Profile updated successfully!")
        return redirect('profile')
    else:
        return redirect('profile')


def logout_view(request):
    logout(request)
    messages.success(request,'Logout successfully!')
    return redirect('login')

def community_page(request):
    return render(request, 'users/community.html')