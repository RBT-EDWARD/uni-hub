from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Community
from .serializers import CommunitySerializer

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    # API to join a community
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        community = self.get_object()
        community.members.add(request.user)
        return Response({'status': 'joined community'})

    # API to leave a community
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        community = self.get_object()
        community.members.remove(request.user)
        return Response({'status': 'left community'})

    # API for keyword search
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            communities = Community.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            communities = Community.objects.all()
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data)