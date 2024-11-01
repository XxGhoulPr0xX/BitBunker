from datetime import datetime
from django.utils import timezone
from django.shortcuts import redirect, render
from .models import RegistroAlServicioSocial, Usuario

def profile(request):
    return render(request,'users/profile.html')

def home(request):
    return render(request,'users/home.html')

def setup(request):
    return render(request,'users/setup.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidoP = request.POST.get('apellidoP')
        apellidoM = request.POST.get('apellidoM')
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')
        semestre = request.POST.get('semestre')
        periodo = request.POST.get('periodo')
        
        usuario = Usuario(
            matricula=matricula,
            nombre=nombre,
            apellidoP=apellidoP,
            apellidoM=apellidoM,
            password=password
        )
        usuario.save()
        año_actual = datetime.now().year
        if periodo == 'A':
            fecha_inicio = timezone.make_aware(datetime(año_actual, 1, 29))
            fecha_finalizacion = timezone.make_aware(datetime(año_actual, 5, 31, 23, 59))
        elif periodo == 'B':
            fecha_inicio = timezone.make_aware(datetime(año_actual, 8, 21))
            fecha_finalizacion = timezone.make_aware(datetime(año_actual, 12, 8, 23, 59))
        else:
            return render(request, 'users/register.html', {'error': 'Periodo no válido'})
        registro_servicio_social = RegistroAlServicioSocial(
            matricula=usuario,
            fechaInicio=fecha_inicio,
            fechaDeFinalizacion=fecha_finalizacion
        )
        registro_servicio_social.save()
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
