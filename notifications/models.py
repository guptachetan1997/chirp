from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class NotificationQuerySet(models.QuerySet):
    def all(self):
        return self.all()

    def unread(self, user):
        return self.filter(Q(status=False) & Q(user_id = user.id))

    def read(self, user):
        return self.filter(Q(status=True) & Q(user_id = user.id))

class NotificationManager(models.Manager):
    def get_qs(self, user):
        return NotificationQuerySet(self.model, using=self._db).order_by('-timestamp')

    def mark_read_all(self, user):
        qs = self.get_qs(user=user).unread(user=user)
        for q in qs:
            q.mark_read()

    def unread_count(self, user):
        return self.get_qs(user=user).unread(user=user).count()


class Notification(models.Model):
    content = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    objects = NotificationManager()

    def __str__(self):
        return str(self.content) + " |to| " + str(self.user.username)

    def mark_read(self):
        self.status = True
        self.save()
