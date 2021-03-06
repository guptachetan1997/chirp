from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Chirp
from .forms import ChirpForm,ChirpReplyForm
from accounts.models import UserProfile
import re

def get_trending_hasgtags():
	trends = {}
	chirps = Chirp.objects.all()
	for chirp_data in chirps:
		text = chirp_data.content
		pat = re.compile(r'[#](\w+)')
		hashtags = pat.finditer(text)
		for hasgtag in hashtags:
			try:
				trends[hasgtag.group().lower()]+=1
			except KeyError:
				trends[hasgtag.group().lower()] = 1
	trending = []
	for w in sorted(trends, key=trends.get, reverse=True):
  		trending.append(dict(hasgtag=w, chirp_count=trends[w]))
	return trending[:3]

@login_required(login_url = '/accounts/login')
def feed(request):
	who_to_follow = request.user.profile.get_who_to_follow()
	trends = get_trending_hasgtags()
	chirpss_data = Chirp.objects.all().filter(parent=None).order_by('-timestamp')
	chirps_data = [chirp_data for chirp_data in chirpss_data if request.user.profile.do_i_follow(chirp_data.user.profile)]
	user_chirps = Chirp.objects.filter(user=request.user).count()
	return render(request, 'chirps/feed.html', {'chirps_data':chirps_data, 'user_chirps':user_chirps, 'trends':trends, 'who_to_follow':who_to_follow})

@login_required(login_url = '/accounts/login')
@csrf_protect
def single_chirp(request, user_username, chirp_id):
	if request.method == 'POST':
		try:
			reply_chirp_obj = Chirp()
			reply_chirp_obj.content = request.POST.get('content')
			reply_chirp_obj.user = User.objects.get(id = int(request.POST.get('chirp_user')))
			parent_id = int(request.POST.get('parent'))
			if parent_id:
				parent_obj = Chirp.objects.filter(id=parent_id)
				if parent_obj is not None:
					reply_chirp_obj.parent = parent_obj.first()
				reply_chirp_obj.save()
		except:
			return HttpResponseRedirect("/%s/%s" % (user_username, chirp_id))
		return HttpResponseRedirect("/%s/%s" % (user_username, chirp_id))
	else:
		chirp_data = Chirp.objects.get(id = chirp_id)
		if chirp_data.is_parent is not True:
			chirp_data = chirp_data.parent
		return render(request, 'chirps/single_chirp.html', {'chirp_data':chirp_data})

@login_required(login_url = '/accounts/login')
@csrf_protect
def add_chirp(request):
	if request.method == 'POST':
		form = ChirpForm(request.POST)
		if form.is_valid():
			chirp_form = form.save(commit = False)
			chirp_form.user = request.user
			chirp_form.save()
		return HttpResponseRedirect("/")
	else:
		args = {}
		args['form'] = ChirpForm()
		return render(request, 'chirps/post_chirp.html', args)

@login_required(login_url = '/accounts/login')
@csrf_protect
def like(request):
	if request.method == 'POST':
		chirp_id = request.POST.get('like', False)
		if chirp_id:
			try:
				req_chirp = Chirp.objects.get(id = chirp_id)
				if req_chirp.like.filter(id = request.user.id).exists():
					req_chirp.like.remove(request.user)
				else:
					req_chirp.like.add(request.user)
			except ObjectDoesNotExist:
				return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')

@login_required(login_url = '/accounts/login')
@csrf_protect
def rechirp(request):
	if request.method == 'POST':
		chirp_id = request.POST.get('rechirp', False)
		if chirp_id:
			try:
				req_chirp = Chirp.objects.get(id = chirp_id)
				new_chirp = Chirp()
				new_chirp = req_chirp
				new_chirp.pk = None
				new_chirp.rechirp_status = True
				new_chirp.origin_chirp_user = req_chirp.user
				new_chirp.user = request.user
				new_chirp.save()
			except ObjectDoesNotExist:
				return HttpResponseRedirect('/')
	return HttpResponseRedirect('/')

@login_required(login_url = '/accounts/login')
def search(request):
	trends = get_trending_hasgtags()
	who_to_follow = request.user.profile.get_who_to_follow()
	query = request.GET.get('search')
	if str(query) is '':
		return HttpResponseRedirect('/')
	pat = re.compile(r'[@](\w+)')
	attags = pat.finditer(query)
	search_profile = None
	for attag in attags:
		try:
			search_profile = User.objects.get(username = attag.group()[1:])
			return HttpResponseRedirect('/accounts/profile/user/%s'%search_profile.username)
		except ObjectDoesNotExist:
			search_profile = None
		break
	search_data = Chirp.objects.filter(content__icontains=query).order_by('-timestamp')
	people = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
	return render(request, 'chirps/search_results.html', {'search_data':search_data, 'query':query, 'search_profile':search_profile, 'people':people, 'trends':trends, 'who_to_follow':who_to_follow})
	#We can differenitate here on the basis of the search query we have got like @ and # or any other textual query
