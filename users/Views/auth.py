from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import Usuario, RegistroAlServicioSocial
from ..Services import getFechasPeriodoEscolar

def login(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')
        try:
            usuario = Usuario.objects.get(matricula=matricula)
            if usuario.password == password:
                request.session['matricula'] = usuario.matricula
                return redirect('home')
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {"datos": "Vuelve a intentarlo"})
    return render(request, 'login.html')

def logout(request):
    if 'matricula' in request.session:
        del request.session['matricula']
        messages.success(request, "Sesión cerrada correctamente.")
    return redirect('inicio')

def register(request):
    if request.method == 'POST':
        datos = {k: request.POST.get(k) for k in ['nombre', 'apellidoP', 'apellidoM', 'matricula', 'password', 'semestre', 'periodo']}
        usuario = Usuario(
            matricula=datos['matricula'],
            nombre=datos['nombre'],
            apellidoP=datos['apellidoP'],
            apellidoM=datos['apellidoM'],
            password=datos['password'],
            semestre=datos['semestre']
        )
        usuario.save()
        fecha_inicio, fecha_fin = getFechasPeriodoEscolar(datos['periodo'])
        if not fecha_inicio:
            return render(request, 'users/register.html', {'error': 'Periodo no válido'})
        RegistroAlServicioSocial.objects.create(
            matricula=usuario,
            fechaInicio=fecha_inicio,
            fechaDeFinalizacion=fecha_fin
        )
        return redirect('login')
    return render(request, 'register.html')