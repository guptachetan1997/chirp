from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

def upload_location(instance, filename):
    u = User.objects.get(id = instance.user_id)
    return "%s/%s" %(str(u.username), filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    bio = models.CharField(max_length = 160, blank=True)
    location = models.CharField(max_length=50, blank=True)
    dob = models.DateField(default="2016-03-03")
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    display_pic = models.ImageField(upload_to=upload_location)

    def __str__(self):
        u = User.objects.get(id = self.user_id)
        return u.username

User.profile = property(lambda u : UserProfile.objects.get_or_create(user=u)[0])
