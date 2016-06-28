from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^register/$', views.UserCreateAPIView.as_view(), name='register'),
	url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
]
