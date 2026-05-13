from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, through='EventRegistration', related_name='attendees')

    def __str__(self):
        return  f"created by {self.organizer},  Event: {self.title}"

class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')