from django.db import models
from communities.models import Community

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
