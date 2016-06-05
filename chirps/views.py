from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from models import chirp
from forms import ChirpForm
from accounts.models import UserProfile
import re

# Create your views here.

@login_required(login_url = '/accounts/login')
def feed(request):
	chirps_data = chirp.objects.all().order_by('-timestamp')
	user_chirps = chirp.objects.filter(user=request.user).count()
	return render(request, 'chirps/feed.html', {'chirps_data':chirps_data, 'user_chirps':user_chirps})

@login_required(login_url = '/accounts/login')
def single_chirp(request, user_username, chirp_id):
	chirp_data = chirp.objects.get(id = chirp_id)
	return render(request, 'chirps/single_chirp.html', {'chirp_data':chirp_data})

@login_required(login_url = '/accounts/login')
@csrf_protect
def add_chirp(request):
	if request.method == 'POST':
		form = ChirpForm(request.POST)
		if form.is_valid():
			chirp_form = form.save(commit = False)
			chirp_form.user = request.user
			chirp.likes = 0
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
				req_chirp = chirp.objects.get(id = chirp_id)
				if req_chirp.like.filter(id = request.user.id).exists():
					req_chirp.like.remove(request.user)
				else:
					req_chirp.like.add(request.user)
			except ObjectDoesNotExist:
				return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')

@login_required(login_url = '/accounts/login')
def search(request):
	query = request.GET.get('search', '')
	pat = re.compile(r'[@](\w+)')
	attags = pat.finditer(query)
	search_profile = None
	for attag in attags:
		flag = User.objects.filter(username = attag.group()[1:])
		if flag.exists():
			search_profile = flag[0]
		break
	search_data = chirp.objects.filter(content__icontains=query).order_by('-timestamp')
	return render(request, 'chirps/search_results.html', {'search_data':search_data, 'query':query, 'search_profile':search_profile})
	#We can differenitate here on the basis of the search query we have got like @ and # or any other textual query
