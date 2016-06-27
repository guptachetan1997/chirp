from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$', views.ChirpListAPIView.as_view(), name='list'),
    url(r'^create/$', views.ChirpCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.ChirpDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.ChirpUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.ChirpDeleteAPIView.as_view(), name='delete'),
]
