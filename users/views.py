from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def profile(request):
    return render(request,'users/profile.html')

def home(request):
    return render(request,'users/home.html')

def registrarse(request):
    return render(request, 'users/registrarse.html')

def login(request):
    return render(request, 'users/login.html')
