from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    location = models.PointField()

    def __str__(self):
        return self.event_name

