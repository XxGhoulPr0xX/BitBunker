from datetime import datetime
import json
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.shortcuts import redirect
from django.shortcuts import render
from .models import RegistroAlServicioSocial, Usuario, RegistroDiario
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
from django.db.models import Sum
from django.contrib import messages


def profile(request):
    matricula = request.session.get('matricula')
    if not matricula:
        return render(request, 'users/profile.html', {"error": "Matrícula no encontrada en la sesión."})
    try:
        usuario = Usuario.objects.get(matricula=matricula)
        total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))
    except Usuario.DoesNotExist:
        return render(request, 'users/profile.html', {"error": "Usuario no encontrado."})
    context = {
        "matricula": matricula,
        "semestre": usuario.semestre,
        "nombre": usuario.nombre,
        "apellidoP": usuario.apellidoP,
        "apellidoM": usuario.apellidoM,
        "horas":total_horas['total']
    }
    return render(request,'users/profile.html',context)

def home(request):
    matricula = request.session.get('matricula')
    total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))
    context = {
        "horasActuales":total_horas['total']
    }
    return render(request,'users/home.html',context)

def setup(request):
    matricula = request.session.get('matricula')
    if not matricula:
        return render(request, 'users/setup.html', {"error": "Matrícula no encontrada en la sesión."})
    try:
        usuario = Usuario.objects.get(matricula=matricula)
    except Usuario.DoesNotExist:
        return render(request, 'users/setup.html', {"error": "Usuario no encontrado."})
    context = {
        "semester": usuario.semestre,
        "first_name": usuario.nombre,
        "middle_name": usuario.apellidoP,
        "last_name": usuario.apellidoM,
    }
    return render(request, 'users/setup.html', context)

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
            password=password,
            semestre=semestre
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
        try:
            usuario = Usuario.objects.get(matricula=matricula)
            if usuario.password == password:
                request.session['matricula'] = usuario.matricula
                return redirect('home')
        except Usuario.DoesNotExist:
            return render(request, 'users/login.html',{"error":"Vuelve a intentarlo"})
    return render(request, 'users/login.html',)

def inicio(request):
    return render(request, 'users/inicio.html')

#Logica:
@csrf_exempt
def save_pdf(request):
    if request.method == "POST":
        data = json.loads(request.body)

        report_number = data.get("reportNumber", "1")
        matricula = request.session.get('matricula')
        registro = RegistroAlServicioSocial.objects.get(matricula=matricula)
        first_name = data.get("firstName", "Nombre")
        middle_name = data.get("middleName", "Apellido Paterno")
        last_name = data.get("lastName", "Apellido Materno")
        semester = data.get("semester", "Semestre")
        total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))

        output_dir = os.path.join("media", "pdf_reports")
        os.makedirs(output_dir, exist_ok=True)  # Crear directorio si no existe
        file_path = os.path.join(output_dir, f"Reporte_{report_number}.pdf")

        c = canvas.Canvas(file_path, pagesize=letter)

        c.drawString(300, 750, f"Reporte No. {report_number}")

        imagen_izquierda_path = os.path.join("static", "users/image/tecnm.jfif")
        imagen_derecha_path = os.path.join("static", "users/image/ser.jfif")
        c.drawImage(imagen_izquierda_path, 50, 700, width=75, height=75)
        c.drawImage(imagen_derecha_path, 500, 700, width=75, height=75)

        data_table = [
            ["No. de Control:",matricula],
            ["Nombre:",first_name],
            ["Apellido Paterno",middle_name],
            ["Apellido Materno", last_name]
        ]
        table = Table(data_table, colWidths=[100, 400])
        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5,colors.black),
                    ("SPAN", (1, 1), (1, 1)),  # Combinar celdas para Apellido Paterno
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ]
            )
        )
        table.wrapOn(c, 50, 610)
        table.drawOn(c, 50, 610)
        fecha_inicio = registro.fechaInicio
        periodo = ""
        if fecha_inicio.month in [1, 2, 3, 4, 5]:  # Meses del Periodo A
            periodo = "A"
        elif fecha_inicio.month in [8, 9, 10, 11, 12]:  # Meses del Periodo B
            periodo = "B"
        periodo_table = [
            [f"Periodo Reportado: {periodo}"],
            ["Del día:", fecha_inicio.day, "Mes", fecha_inicio.strftime("%B"), fecha_inicio.year],
            ["Al día:", registro.fechaDeFinalizacion.day, "Mes", registro.fechaDeFinalizacion.strftime("%B"), registro.fechaDeFinalizacion.year],
        ]
        periodo = Table(periodo_table, colWidths=[200, 50, 50, 100, 100])
        periodo.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("SPAN", (0, 0), (4, 0)),  # Combinar celdas del título
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ]
            )
        )
        periodo.wrapOn(c, 50, 520)
        periodo.drawOn(c, 50, 520)

        textos = [
            f"El presente documento certifica que el/la estudiante {first_name} {middle_name} {last_name}",
            f"De {semester}° semestre, con número de matrícula {matricula}",
            f"ha cumplido satisfactoriamente con las {total_horas['total']} horas de servicio social requeridas.",
            f"Para realizar el informe {report_number}°"
        ]
        for i in range(len(textos)):
            c.drawString(50, 500-(i*15), textos[i])
        c.save()

        return redirect('home')
    else:
        return redirect('setup')

@csrf_exempt
def contador(request):
    if request.method == 'POST':  # Validamos que el método sea POST
        matricula = request.session.get('matricula')
        if not matricula:
            return JsonResponse({"error": "Matrícula no encontrada en la sesión."}, status=400)
        try:
            usuario = Usuario.objects.get(matricula=matricula)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado."}, status=404)
        fecha = now().date()  # Obtenemos solo la fecha actual
        if RegistroDiario.objects.filter(matricula=usuario, fecha=fecha).exists():
            total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))
            return JsonResponse({"error": "Ya existe un registro para el día de hoy.", "horasTotales": total_horas['total']}, status=400)
        else:        
            horaEntrada = now()  # Hora actual
            horaSalida = horaEntrada + timedelta(hours=4)  # Calculamos la hora de salida como 4 horas después
            contador = RegistroDiario(
                matricula=usuario,
                fecha=fecha,
                horaEntrada=horaEntrada,
                horaSalida=horaSalida,
                horasDiaria=4
            )
            contador.save()
            total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))
            return JsonResponse({
                "message": "Horas registradas correctamente.",
                "horasTotales": total_horas['total']
            }, status=201)
    return JsonResponse({"error": "Método no permitido."}, status=405)

def logout(request):
    if 'matricula' in request.session:
        del request.session['matricula']
    messages.info(request,'Sesión cerrada')
    return redirect('inicio')