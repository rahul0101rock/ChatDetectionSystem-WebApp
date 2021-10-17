from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp, name='signup'),
    path('logout/', views.logOut, name='logout'),
    path('login/', views.logIn, name='login'),
    path('profile/', views.profile, name='profile'),
]