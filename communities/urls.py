from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # 👈 This line is required
from .views import CommunityViewSet

router = DefaultRouter()
router.register(r'communities', CommunityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:community_id>/posts/', views.post_list, name='post_list'),
    path('<int:community_id>/posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]