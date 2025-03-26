from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/<int:pk>',views.update_profile,name="update_profile"),
]
