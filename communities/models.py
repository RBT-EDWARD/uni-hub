from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    meeting_details = models.TextField(blank=True, null=True)  # <-- Add this
    interest_tags = models.CharField(max_length=200, blank=True) 
    members = models.ManyToManyField(User, related_name='communities', blank=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="led_communities")
    
    def __str__(self):
        return self.name
