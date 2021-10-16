from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
# Create your views here.

def home(request):
    return render(request,'chatsys/home.html',{})

def signUp(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
    	if request.method =='POST':
    		form = SignUpForm(request.POST)
    		if form.is_valid():
    			form.save()
    			username = form.cleaned_data['username']
    			password = form.cleaned_data['password1']
    			user = authenticate(username=username, password=password)
    			login(request,user)
    			return redirect('/')
    	else:
    		form = SignUpForm()
    	return render(request, 'chatsys/signup.html', {'form': form})


def logOut(request):
    if request.user.is_authenticated:
    	logout(request)
    return redirect('/')

