from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from communities.models import Community
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("Inside the valide form")
            user = form.save()
            # create the profile instance
            Profile.objects.create(
                user=user,
                bio=form.cleaned_data['bio'],
                interests=form.cleaned_data['interests']
            )
            print('Returning')
            messages.success(request, "Register successful!,Please login into your accont.")
            return redirect('login')
        else:
            print("Inside else :- form is not valid")
            print(form.errors)
            for field, errors in form.errors.items():
                print(errors)
            return render(request, 'users/register.html', {"form": form})
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
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'users/login.html')

def index_view(request):
    return render(request, "users/index_page.html")

# the view of the home page.
def home_view(request):
    latest_communities = Community.objects.prefetch_related('members').order_by('-id')[:3]
    latest_events = Event.objects.prefetch_related('participants').order_by('-id')[:3]

    return render(request, 'users/home_page.html', {
        'latest_communities': latest_communities,
        'latest_events': latest_events
    })

def profile_view(request):
    print("Logged in user:- ", request.user, request.user.id)
    logged_in_user_profile = Profile.objects.get(user=request.user)
    return render(request, "users/profile_page.html", {"profile": logged_in_user_profile})

def update_profile(request, pk):
    selectedProfile = Profile.objects.get(id=pk)
    if request.method == "POST":
        userEmail = request.POST["useremail"]
        userBio = request.POST["bio"]
        userInterest = request.POST["interests"]

        selectedProfile.user.email = userEmail
        selectedProfile.bio = userBio
        selectedProfile.interests = userInterest
        selectedProfile.save()
        selectedProfile.user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    else:
        return redirect('profile')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('login')

def community_page(request):
    query = request.GET.get("q", "")
    if query:
        communities = Community.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        communities = Community.objects.all()

    return render(request, "users/community.html", {'communities': communities, 'search_query': query})

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.add(request.user)
    messages.success(request, f"You have joined the community: {community.name}")

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
        return redirect(next_url)
    return redirect('community_page')

@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.remove(request.user)
    messages.success(request, f"You have left the community: {community.name}")

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
        return redirect(next_url)
    return redirect('community_page')

def event_page(request):
    events = Event.objects.all()
    communities = Community.objects.all()
    query_text = request.GET.get("querytext", "")
    filter_date = request.GET.get("filter_date", "")
    filter_community = request.GET.get("filter_community", "")

    # Apply Filters
    if query_text:
        events = events.filter(
            Q(title__icontains=query_text) |
            Q(description__icontains=query_text)
        )

    if filter_date:
        try:
            parsed_date = datetime.strptime(filter_date, "%Y-%m-%d").date()
            events = events.filter(date__date=parsed_date)
        except ValueError:
            pass  # This will ignore invalid date

    if filter_community:
        events = events.filter(community_id=filter_community)

    return render(request, 'users/event.html', {
        'events': events,
        'communities': communities,
        'query_text': query_text,
    })

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
        messages.success(request, f"You have successfully joined the event: {event.title}")
    else:
        messages.info(request, "You have already joined this event.")

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
        return redirect(next_url)
    return redirect("event_page")

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.success(request, f"You have left the event: {event.title}")
    else:
        messages.warning(request, "You were not a participant of this event.")

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
        return redirect(next_url)
    return redirect("event_page")
