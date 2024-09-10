from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('users.urls')),  # Aquí asegúrate de incluir las rutas de tu aplicación.
    path('admin', admin.site.urls),
]
