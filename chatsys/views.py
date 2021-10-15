from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .forms import SignUpForm
# Create your views here.

def home(request):
    return render(request,'chatsys/home.html',{})

def signUp(request):
    form = SignUpForm()
    return render(request, 'chatsys/signup.html', {'form': form})