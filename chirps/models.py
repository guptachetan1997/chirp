from __future__ import unicode_literals
import re
import urllib
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import bleach

# Create your models here.

class Chirp(models.Model):
	content = models.CharField(max_length=140)
	timestamp = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User)
	like = models.ManyToManyField(User, related_name='likes', blank=True)
	rechirp_status = models.BooleanField(default = False)
	origin_chirp_user = models.ForeignKey(User, blank = True, null=True, related_name="ori_chirp_by")
	parent = models.ForeignKey("self", null=True, blank=True)

	def __str__(self):
		return self.content[:140]

	def save(self, *args, **kwargs):
		super(Chirp, self).save(*args, **kwargs)
		from notifications.models import new_notification
		mentions = self.get_mentions()
		if mentions:
			verb = "mentioned you"
			new_notification(
			    origin_user = self.user.username,
			    affected_users = mentions,
			    verb=verb,
			    target=self,
			    )

	def children(self):
		return Chirp.objects.filter(parent=self).order_by("-timestamp")

	@property
	def is_parent(self):
		if self.parent == None:
			return True
		return False

	@property
	def reply_count(self):
		return Chirp.objects.filter(parent=self).count()

	def get_mentions(self):
		text = self.content
		pattern = re.compile(r'[@](\w+)')
		mentions = pattern.finditer(text)
		mention_list = []
		for mention in mentions:
			username = mention.group()[1:]
			try:
				mention_list.append(User.objects.get(username=username))
			except User.DoesNotExist:
				print ("Shame")
		return mention_list

	def html_tags_edit(self):
		text = self.content
		attrs = {
     		'*': ['class'],
     		'a': ['href', 'rel'],
     		'img': ['alt', 'src'],
 		}
		try:
			final_text = ""
			pat = re.compile(r'[#,@](\w+)')
			hashtags = pat.finditer(text)
			i=0
			for hasgtag in hashtags:
				search_query = "\'" + "/search?search=" + urllib.quote(hasgtag.group()) + "\'"
				final_text += (text[i:hasgtag.span()[0]] + "<a href=" + search_query + ">" + hasgtag.group() + "</a>")
				i = hasgtag.span()[1]
			final_text += (text[i:])
			if final_text == "":
				text = bleach.clean(text, tags=['img', 'a'], attributes=attrs, strip=True)
				text = bleach.linkify(text)
				return mark_safe(text)
			else:
				final_text = bleach.clean(final_text, tags=['img', 'a'], attributes=attrs, strip=True)
				final_text = bleach.linkify(final_text)
				return mark_safe(final_text)
		except:
			return text
