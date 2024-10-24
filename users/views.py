from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Usuario

def profile(request):
    return render(request,'users/profile.html')

def home(request):
    return render(request,'users/home.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidoP = request.POST.get('apellidoP')
        apellidoM = request.POST.get('apellidoM')
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')

        usuario = Usuario(
            matricula=matricula,
            nombre=nombre,
            apellidoP=apellidoP,
            apellidoM=apellidoM,
            password=password
        )
        usuario.save()
        return redirect('login') 
    return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')
        print(f"Datos ingresados: Matrícula={matricula}, Contraseña={password}")
        try:
            usuario = Usuario.objects.get(matricula=matricula)
            if usuario.password == password:
                request.session['matricula'] = usuario.matricula
                print("Inicio de sesión exitoso")
                return redirect('home')
            else:
                print("Contraseña incorrecta")
        except Usuario.DoesNotExist:
            print("Usuario no encontrado")
    return render(request, 'users/login.html')

def inicio(request):
    return render(request, 'users/inicio.html')
