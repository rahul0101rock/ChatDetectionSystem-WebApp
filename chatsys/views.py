import pyrebase
#from django.http import HttpResponse
#from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
import datetime,pytz

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import nltk
nltk.download('subjectivity')
nltk.download('vader_lexicon')
n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
train_docs = subj_docs + obj_docs
sentim_analyzer = SentimentAnalyzer()
all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in train_docs])
unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
training_set = sentim_analyzer.apply_features(train_docs)
trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, training_set)
sia = SentimentIntensityAnalyzer()
# Create your views here.
config={
  "apiKey": "AIzaSyDCem5mrJqfv3phnowuLY1EK5vIzHdiY1o",
  "authDomain": "chat-detection-system.firebaseapp.com",
  "databaseURL": "https://chat-detection-system-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "chat-detection-system",
  "storageBucket": "chat-detection-system.appspot.com",
  "messagingSenderId": "464189634762",
  "appId": "1:464189634762:web:a726a15005bf5edd739c33",
  "measurementId": "G-3H7P7CP7T1"
}
IST = pytz.timezone('Asia/Kolkata')
firebase=pyrebase.initialize_app(config)
db=firebase.database()

def home(request):
    data={}
    if request.user.is_authenticated:
        allusers={}
        sus_users=db.child("Suspicious_users").child(request.user.username).get().val();
        sus_users = sus_users.keys() if sus_users else []
        data["sus"] = sus_users
        for u in User.objects.all():
            if not (u.username == request.user.username or u.username == "admin" or u.username in sus_users):
                allusers[u.username]=u.first_name+" "+u.last_name
        data["Users"]=allusers
        chats={}
        if request.method == 'POST':
            receiver = request.POST['receiver']
            mk = "-".join(sorted([request.user.username,receiver]))

            if 'sendmsg' in request.POST and request.POST['message']:
                message = request.POST['message'].strip()
                if len(message)>0:
                    Datetime = str(datetime.datetime.now(IST))[:-13]
                    ss = sia.polarity_scores(message)
                    if ss["neg"]:
                        db.child("Suspicious_users").child(receiver).child(request.user.username).update({"sus_user": True})
                    msg={
                        "Sender": request.user.username,
                        "Receiver": receiver,
                        "dateTime": Datetime,
                        "Message": message,
                        "sus": ss["neg"]
                    }
                    db.child("Chats").child(mk).push(msg)
            dbchat=db.child("Chats").child(mk).get().val()
            if dbchat:
                chats=dbchat.values()
            data["rec"]=receiver
            if chats:
                data["Chats"]=zip(chats,[c["Sender"]==request.user.username for c in chats])
        return render(request,'chatsys/chat.html',data)
    else:
        return render(request,'chatsys/home.html',data)

def susUsers(request):
    if request.user.is_authenticated:
        data={}
        allusers={}
        sus_users=db.child("Suspicious_users").child(request.user.username).get().val();
        sus_users = sus_users.keys() if sus_users else []
        for u in User.objects.all():
            if not (u.username == request.user.username or u.username == "admin" or not u.username in sus_users):
                allusers[u.username]=u.first_name+" "+u.last_name
        data["Users"] = allusers
        data["No_SUS"] = True
        if len(allusers) == 0:
            return render(request,'chatsys/chat.html',data)
        chats={}
        if request.method == 'POST':
            receiver = request.POST['receiver']
            mk = "-".join(sorted([request.user.username,receiver]))

            if 'sendmsg' in request.POST and request.POST['message']:
                message = request.POST['message'].strip()
                if len(message)>0:
                    Datetime = str(datetime.datetime.now(IST))[:-13]
                    ss = sia.polarity_scores(message)
                    if ss["neg"]:
                        db.child("Suspicious_users").child(receiver).child(request.user.username).update({"sus_user": True})
                    msg={
                        "Sender": request.user.username,
                        "Receiver": receiver,
                        "dateTime": Datetime,
                        "Message": message,
                        "sus": ss["neg"]
                    }
                    db.child("Chats").child(mk).push(msg)
            dbchat=db.child("Chats").child(mk).get().val()
            if dbchat:
                chats=dbchat.values()
            data["rec"]=receiver
            if chats:
                data["Chats"]=zip(chats,[c["Sender"]==request.user.username for c in chats])
        return render(request,'chatsys/chat.html',data)
    else:
        return redirect('/')


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
    			db.child("Bio").child(request.user).update({"bio":"Hello there!"})
    			return redirect('/')
    	else:
    		form = SignUpForm()
    	return render(request, 'chatsys/signup.html', {'form': form})

def logIn(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.error(request, 'Username or Password is Incorrect')
                return redirect('login')
        else:
            return render(request,'chatsys/login.html',{})

def logOut(request):
    if request.user.is_authenticated:
    	logout(request)
    return redirect('/')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        if request.method == 'POST':
            bio = request.POST['bio']
            db.child("Bio").child(request.user).update({"bio":bio})
            if db.child("Bio").child(request.user).get().val()['bio']==bio:
                messages.success(request, 'Bio Updated')

        data={}
        data["bio"]=db.child("Bio").child(request.user).get().val()['bio']
        data["imgurl"]="https://avatars.dicebear.com/api/initials/" +request.user.first_name+ "%20" +request.user.last_name+".svg"
        return render(request,'chatsys/profile.html',data)