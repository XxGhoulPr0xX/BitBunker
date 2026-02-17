from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # 1. Corregido: admin.site.urls es el estándar de Django
    path('admin/', admin.site.urls), 
    
    # 2. Tus rutas de la aplicación 'users'
    path('', include('users.urls')),
    
    # 3. Redirección de la raíz (http://localhost:8080/) hacia /login/
    path('', RedirectView.as_view(url='/register/'), name='index_redirect'), 
]