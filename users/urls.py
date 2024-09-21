from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('home/', home, name="Home"),
    path('register/', register, name="register"),
    path('login/',login,name="login")
    ]
