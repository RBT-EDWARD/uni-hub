from django.db import models 
from django.contrib.auth.models import User

class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    meeting_details = models.TextField(blank=True, null=True)
    interest_tags = models.CharField(max_length=200, blank=True)
    members = models.ManyToManyField(User, related_name='communities', blank=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="led_communities")

    def __str__(self):
        return self.name

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('members', 'Community Members Only'),
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255, help_text="Comma-separated tags (e.g., study, math, group)")
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    attachment = models.FileField(upload_to='post_attachments/', blank=True, null=True)  # for attachments

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
