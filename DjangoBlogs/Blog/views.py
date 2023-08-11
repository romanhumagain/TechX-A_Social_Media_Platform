from django.shortcuts import render
from django.http import HttpResponse
from Blog.models import *
# Create your views here.

def home(request):
  context = {
    'posts':BlogPost.objects.order_by('-date_posted')
  }
  return render(request ,'blog/home.html',context )

def about(request):
  return render(request ,'blog/about.html',{'title':"About"} )