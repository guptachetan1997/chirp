from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^login', views.log_in),
    url(r'^auth_view', views.auth_view),
    url(r'^logout', views.log_out),
    url(r'^register', views.register),
    url(r'^profile/user/(?P<user_username>\w+)$', views.user_profile_display),
    url(r'^profile/edit', views.user_profile_edit),
    url(r'^profile/follow', views.user_follow),
    url(r'^profile/unfollow', views.user_unfollow),
]
