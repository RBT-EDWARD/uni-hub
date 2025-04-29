from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib.auth.models import User
from .forms import UserRegisterForm, CommunityForm 

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save User model
            user = form.save()

            # Save extended profile data
            Profile.objects.create(
                user=user,
                address=form.cleaned_data['address'],
                dob=form.cleaned_data['dob'],
                interests=form.cleaned_data['interests']
            )

            messages.success(request, "Register successful! Please login into your account.")
            return redirect('login')
        else:
            return render(request, 'users/register.html', {"form": form})
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'users/login.html')

# Index Landing Page
def index_view(request):
    return render(request, "users/index_page.html")

# Home Page with Search + Latest Communities/Events
def home_view(request):
    latest_communities = Community.objects.prefetch_related('members').order_by('-id')[:3]
    latest_events = Event.objects.prefetch_related('participants').order_by('-id')[:3]
    search_query = request.GET.get('q', '')
    matching_profiles = []

    if search_query:
        matching_profiles = Profile.objects.filter(interests__icontains=search_query)

    return render(request, 'users/home_page.html', {
        'latest_communities': latest_communities,
        'latest_events': latest_events,
        'search_query': search_query,
        'matching_profiles': matching_profiles,
    })

def community_detail(request, pk):
    community = get_object_or_404(Community, id=pk)
    return render(request, 'users/community_detail.html', {'community': community})

@login_required
def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            community.members.add(request.user)
            messages.success(request, f"Community '{community.name}' created successfully!")
            return redirect('community_page')
    else:
        form = CommunityForm()
    return render(request, 'users/create_community.html', {'form': form})

# Profile View
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "users/profile_page.html", {"profile": profile})

# Profile Update View
@login_required
def update_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    if request.method == "POST":
        profile.user.email = request.POST.get("useremail")
        profile.program = request.POST.get("program")
        profile.year = request.POST.get("year")
        profile.interests = request.POST.get("interests")
        profile.campus_involvement = request.POST.get("campus_involvement")
        profile.achievements = request.POST.get("achievements")
        profile.address = request.POST.get("address")
        profile_picture = request.FILES.get("profile_picture")

        dob_input = request.POST.get("dob")
        if dob_input:
            try:
                profile.dob = dob_input
            except ValueError:
                messages.warning(request, "Invalid DOB format. Please use YYYY-MM-DD.")

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.user.save()
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return redirect('profile')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('login')

# Communities List + Search
def community_page(request):
    query = request.GET.get("q", "")
    if query:
        communities = Community.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        communities = Community.objects.all()

    return render(request, "users/community.html", {'communities': communities, 'search_query': query})

# Join Community
@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.add(request.user)
    messages.success(request, f"You have joined the community: {community.name}")

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
        return redirect(next_url)
    return redirect('community_page')

# Leave Community
@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.remove(request.user)
    messages.success(request, f"You have left the community: {community.name}")

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
        return redirect(next_url)
    return redirect('community_page')

# Events View + Filters
def event_page(request):
    events = Event.objects.all()
    communities = Community.objects.all()

    query_text = request.GET.get("querytext", "")
    filter_date = request.GET.get("filter_date", "")
    filter_community = request.GET.get("filter_community", "")

    if query_text:
        events = events.filter(Q(title__icontains=query_text) | Q(description__icontains=query_text))
    if filter_date:
        try:
            parsed_date = datetime.strptime(filter_date, "%Y-%m-%d").date()
            events = events.filter(date__date=parsed_date)
        except ValueError:
            pass
    if filter_community:
        events = events.filter(community_id=filter_community)

    return render(request, 'users/event.html', {
        'events': events,
        'communities': communities,
        'query_text': query_text,
    })

# Join Event
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

# Leave Event
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

# Search Users by Interest
@login_required
def search_users(request):
    query = request.GET.get('q', '')
    results = Profile.objects.filter(interests__icontains=query) if query else []
    return render(request, 'users/search.html', {'results': results, 'query': query})
