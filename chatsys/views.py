from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request,'chatsys/home.html',{})