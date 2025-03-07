from django.shortcuts import render
from rest_framework import viewsets
from .models import Community
from .serializers import CommunitySerializer
# Create your views here.


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
