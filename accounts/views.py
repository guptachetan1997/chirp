from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
from forms import RegistrationForm
from django.contrib import messages
from forms import UserProfileForm
from models import UserProfile
from chirps.models import chirp

@csrf_protect
def log_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    args = {}
    return render(request, 'accounts/log_in.html', args)

def auth_view(request):
    username = request.POST.get('inputUsername', "")
    password = request.POST.get('inputPassword', "")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        if UserProfile.objects.filter(user_id= request.user.id).exists():
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/accounts/profile/edit')
    else:
        messages.warning(request, "Invalid credentials")
        return HttpResponseRedirect('/accounts/login')

@login_required(login_url = '/accounts/login')
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")

@csrf_protect
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        flag = 1
        if form.is_valid() == False:
            messages.warning(request, "Enter all credentials correctly")
            flag=0
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.warning(request, "Username is already registered")
            flag=0
        if User.objects.filter(email=request.POST.get('email')).exists():
            messages.warning(request, "Email is already registered")
            flag=0
        if flag is 0:
            return HttpResponseRedirect('/accounts/register')
        form.save()
        return HttpResponseRedirect('/accounts/login')
    else:
        args = {}
        args['form'] = RegistrationForm()
        return render(request, 'accounts/register.html', args)

@csrf_protect
@login_required(login_url='/accounts/login/')
def user_profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        if form.is_valid():
            user_profile_form = form.save(commit = False)
            user_profile_form.user = User.objects.get(id = request.user.id)
            user_profile_form.save()
            return HttpResponseRedirect('/accounts/profile/user/%s'%request.user.username)
        else:
            return HttpResponseRedirect('accounts/profile/edit')
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)
        args = {}
        args['form'] = form
        return render(request, 'accounts/profile_edit.html', args)

@csrf_protect
@login_required(login_url='/accounts/login')
def user_follow(request):
    if request.method == 'POST':
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id = follow_id)
                request.user.profile.follows.add(user.profile)
                return HttpResponseRedirect('/accounts/profile/user/%s'%user.username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

@csrf_protect
@login_required(login_url='/accounts/login')
def user_unfollow(request):
    if request.method == 'POST':
        unfollow_id = request.POST.get('unfollow', False)
        if unfollow_id:
            try:
                user = User.objects.get(id = unfollow_id)
                request.user.profile.follows.remove(user.profile)
                return HttpResponseRedirect('/accounts/profile/user/%s'%user.username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

@csrf_protect
@login_required(login_url='/accounts/login/')
def user_profile_display(request, user_username):
    profile_basics = User.objects.get(username = user_username)
    profile_contents = UserProfile.objects.get(user_id = profile_basics.id)
    user_info = {}
    user_info['chirps_data'] = chirp.objects.filter(user_id = profile_basics.id)
    user_info['chirp_count'] = user_info['chirps_data'].count()
    user_info['mentions'] = chirp.objects.filter(Q(content__icontains='@'+str(profile_basics.username)) & ~Q(user = profile_basics))
    user_info['mention_count'] = user_info['mentions'].count()
    user_info['followers'] = profile_basics.profile.followed_by.all()
    user_info['follower_count'] = user_info['followers'].count()
    user_info['ifollowthem'] = profile_basics.profile.follows.all()
    user_info['ifollowthem_count'] = user_info['ifollowthem'].count()
    user_info['ifollowthemflag'] = False
    if request.user.profile.follows.filter(user__username=user_username):
        user_info['ifollowthemflag'] = True
    return render(request, 'accounts/profile_display.html' , {'profile_contents': profile_contents, 'profile_basics':profile_basics, 'user_info':user_info})
