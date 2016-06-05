from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.feed),
	url(r'^(?P<user_username>\w+)/(?P<chirp_id>\w+)/$', views.single_chirp),
	url(r'^post_chirp/$', views.add_chirp),
	url(r'^search', views.search, name='search'),
	url(r'^like', views.like)
]
