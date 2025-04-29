from django.db import models
from communities.models import Community
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='joined_events', blank=True)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    materials = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
