from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
    content = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=500)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.content
