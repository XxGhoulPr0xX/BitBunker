from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('home/', home, name="home"),
    path('register/', register, name="register"),
    path('login/',login,name="login"),
    path('setup/',setup,name="setup"),
    path('',inicio,name="inicio"),
    path('save_pdf/', save_pdf, name='save_pdf'),
    path('contador/', contador, name='contador'),
    path('logout/', logout, name='logout'),
    ]
