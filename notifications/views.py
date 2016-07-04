from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def all(request):
    return HttpResponseRedirect('http://www.google.com')
