from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Community, Post, Comment
from .serializers import CommunitySerializer
from .forms import PostForm, CommentForm

# API Views using DRF
class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        community = self.get_object()
        community.members.add(request.user)
        return Response({'status': 'joined community'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        community = self.get_object()
        community.members.remove(request.user)
        return Response({'status': 'left community'})

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        communities = Community.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else Community.objects.all()
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data)

@login_required
def create_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.community = community
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_list', community_id=community.id)
    else:
        form = PostForm()

    return render(request, 'communities/post_form.html', {
        'form': form,
        'community': community
    })


def post_list(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = community.posts.order_by('-created_at')

    search_query = request.GET.get('q', '')
    if search_query:
        posts = posts.filter(tags__icontains=search_query)

    return render(request, 'communities/post_list.html', {
        'community': community,
        'posts': posts,
        'search_query': search_query,
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by('created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'communities/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })