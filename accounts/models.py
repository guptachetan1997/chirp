from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

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
    display_pic = models.ImageField(upload_to=upload_location, default="http://santetotal.com/wp-content/uploads/2014/05/default-user.png")

    def __str__(self):
        u = User.objects.get(id = self.user_id)
        return u.username

    def do_i_follow(self, query_profile):
        if query_profile in self.follows.all():
            return True
        else:
            return False

    def get_who_to_follow(self):
    	who_to_follow = []
    	users = User.objects.filter(~Q(username=self.user.username))
    	for user in users:
    		if not self.do_i_follow(user.profile):
    			who_to_follow.append(user)
    	return who_to_follow[:5]


User.profile = property(lambda u : UserProfile.objects.get_or_create(user=u)[0])
