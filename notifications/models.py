from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from chirps.models import Chirp
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

"""
origin_user = who generates the new_notification(username)
affected_users = list of users who get this new_notification(usernames)
verb = this purpose of the new_notification(string)
target = type of notif ie chirp or user(content type)

"""
def new_notification(origin_user, affected_users, verb, target):
    new_notif = Notification()
    if isinstance(target, Chirp):
        new_notif.content =  str(origin_user) + " " + verb
        new_notif.url = "/%s/%s/"%(target.user.username, target.id)
    elif isinstance(target, User):
        new_notif.content = str(origin_user) + " " + verb + " you."
        new_notif.url = "/accounts/profile/user/%s/"%(target.user.username)

    for single_user in affected_users:
        final_notif = new_notif
        final_notif.user = single_user
        final_notif.save()


"""
Notification Generation Doc

from chirps.models import chirp
from django.contrib.auth.models import User
from notifications.models import new_notification

user_data = User.objects.get(username = "chetan1997")
chirp_data = chirp.objects.get(id=67)
verb = "replied to"
affected_users_data = [User.objects.get(username = "abctest123")]

new_notification(
    origin_user = user_data.username,
    affected_users = affected_users_data,
    verb=verb,
    target=chirp_data,
    )
"""
