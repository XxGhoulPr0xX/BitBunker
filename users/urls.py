from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('home/', home, name="Home"),
    path('registrarse', registrarse, name="registrarse"),
    path('minecraft', minecraft, name="minecraft")
]
