from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login')
def all(request):
    all_notifs = Notification.objects.get_qs(user = request.user)
    unread_notifs =  all_notifs.unread(user=request.user)
    read_notifs = all_notifs.read(user=request.user)
    return render(request, 'notifications/all_display.html', {'unread_notifs':unread_notifs, 'read_notifs':read_notifs})

@login_required(login_url='/accounts/login')
def all_read(request):
    Notification.objects.mark_read_all(user=request.user)
    return HttpResponseRedirect('/notifications/all/')
