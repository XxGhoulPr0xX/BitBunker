from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('home/', home, name="home"),
    path('register/', register, name="register"),
    path('login/',login,name="login"),
    path('',inicio,name="inicio")
    ]
