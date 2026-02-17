from django.shortcuts import render
from django.db.models import Sum
from ..models import Usuario, RegistroDiario

def inicio(request):
    return render(request, 'inicio.html')

def home(request):
    matricula = request.session.get('matricula')
    total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))
    horas_finales = total_horas['total'] or 0
    return render(request, 'home.html', {"horasActuales": horas_finales})

def profile(request):
    matricula = request.session.get('matricula')
    if not matricula:
        return render(request, 'profile.html', {"error": "Matrícula no encontrada."})
    try:
        usuario = Usuario.objects.get(matricula=matricula)
        total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))
    except Usuario.DoesNotExist:
        return render(request, 'profile.html', {"error": "Usuario no encontrado."})
    
    context = {
        "matricula": matricula,
        "semestre": usuario.semestre,
        "nombre": usuario.nombre,
        "apellidoP": usuario.apellidoP,
        "apellidoM": usuario.apellidoM,
        "horas": total_horas['total']
    }
    return render(request, 'profile.html', context)

def setup(request):
    matricula = request.session.get('matricula')
    if not matricula:
        return render(request, 'setup.html', {"error": "Error de sesión."})
    try:
        usuario = Usuario.objects.get(matricula=matricula)
        context = {
            "semester": usuario.semestre,
            "first_name": usuario.nombre,
            "middle_name": usuario.apellidoP,
            "last_name": usuario.apellidoM,
        }
        return render(request, 'setup.html', context)
    except Usuario.DoesNotExist:
        return render(request, 'setup.html', {"error": "Usuario no encontrado."})