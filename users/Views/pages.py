from django.shortcuts import redirect, render
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
        "horas": total_horas['total'] or 0
    }
    return render(request, 'profile.html', context)

def setup(request):
    matricula = request.session.get('matricula')
    if not matricula:
        return render(request, 'setup.html', {"error": "Error de sesión."})
    try:
        usuario = Usuario.objects.get(matricula=matricula)
        mensaje_exito = "" 
        if request.method == 'POST':
            usuario.semestre = request.POST.get('semester')
            usuario.nombre = request.POST.get('firstName')
            usuario.apellidoP = request.POST.get('middleName')
            usuario.apellidoM = request.POST.get('lastName')
            usuario.save()
            mensaje_exito = "Datos modificados correctamente"
        return render(request, 'setup.html',         
        {
            "semester": usuario.semestre,
            "first_name": usuario.nombre,
            "middle_name": usuario.apellidoP,
            "last_name": usuario.apellidoM,
            "mensaje": mensaje_exito
        })
    except Usuario.DoesNotExist:
        return render(request, 'setup.html', {"error": "Usuario no encontrado."})