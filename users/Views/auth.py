from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password # Importar herramientas de seguridad
from ..models import Usuario, RegistroAlServicioSocial
from ..Services import getFechasPeriodoEscolar

def login(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')
        try:
            usuario = Usuario.objects.get(matricula=matricula)
            if check_password(password, usuario.password):
                request.session['matricula'] = usuario.matricula
                return redirect('home')
            else:
                return render(request, 'login.html', {"datos": "Matrícula o contraseña incorrecta"})
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {"datos": "No encontramos ninguna cuenta con esa matrícula."})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        datos = {k: request.POST.get(k) for k in ['nombre', 'apellidoP', 'apellidoM', 'matricula', 'password', 'semestre', 'periodo']}
        if Usuario.objects.filter(matricula=datos['matricula']).exists():
            return render(request, 'register.html', {'error': 'El usuario con esta matrícula ya existe.'})
        hashed_password = make_password(datos['password'])
        usuario = Usuario(
            matricula=datos['matricula'],
            nombre=datos['nombre'],
            apellidoP=datos['apellidoP'],
            apellidoM=datos['apellidoM'],
            password=hashed_password,
            semestre=datos['semestre']
        )
        usuario.save()
        fecha_inicio, fecha_fin = getFechasPeriodoEscolar(datos['periodo'])
        if not fecha_inicio:
            return render(request, 'register.html', {'error': 'Periodo no válido'})
            
        RegistroAlServicioSocial.objects.create(
            matricula=usuario,
            fechaInicio=fecha_inicio,
            fechaDeFinalizacion=fecha_fin
        )
        return render(request, 'login.html', {"mensaje": "Cuenta creada correctamente"})
    return render(request, 'register.html')

def logout(request):
    if 'matricula' in request.session:
        del request.session['matricula']
        messages.success(request, "Sesión cerrada correctamente.")
    return redirect('inicio')