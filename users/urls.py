from django.urls import path
from . import views
from .views import create_community
from .views import community_detail

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/<int:pk>',views.update_profile,name="update_profile"),
    path('community/', views.community_page, name='community_page'),
    path('community/join/<int:community_id>/', views.join_community, name='join_community'),
    path('community/leave/<int:community_id>/', views.leave_community, name='leave_community'),
    path('event/', views.event_page, name='event_page'),
    path('event/<int:event_id>/join/', views.join_event, name='join_event'),
    path('event/<int:event_id>/leave/', views.leave_event, name='leave_event'),
    path('search/', views.search_users, name='search_users'),
    path('create-community/', create_community, name='create_community'),
    path('communities/<int:pk>/', views.community_detail, name='community_detail'),
    path("leader/dashboard/", views.leader_dashboard, name="leader_dashboard"),
    path("leader/community/<int:community_id>/event/create/", views.create_event, name="create_event"),
]
