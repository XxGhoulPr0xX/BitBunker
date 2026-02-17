from django.urls import path
from . import Views

urlpatterns = [
    path('profile/', Views.profile, name="profile"),
    path('home/', Views.home, name="home"),
    path('register/', Views.register, name="register"),
    path('login/',Views.login,name="login"),
    path('setup/',Views.setup,name="setup"),
    path('',Views.inicio,name="inicio"),
    path('save_pdf/', Views.save_pdf, name='save_pdf'),
    path('contador/', Views.contador, name='contador'),
    path('logout/', Views.logout, name='logout'),
    ]
