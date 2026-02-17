import os
import io  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.db.models import Sum
from ..models import RegistroAlServicioSocial, RegistroDiario

def GenerarPDF(data, matricula):
    registro = RegistroAlServicioSocial.objects.get(matricula__matricula=matricula)
    total_horas = RegistroDiario.objects.filter(matricula_id=matricula).aggregate(total=Sum('horasDiaria'))
    
    report_number = data.get("reportNumber", "1")
    first_name = data.get("firstName", "Nombre")
    middle_name = data.get("middleName", "Apellido Paterno")
    last_name = data.get("lastName", "Apellido Materno")
    semester = data.get("semester", "Semestre")

    buffer = io.BytesIO() 
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(300, 750, f"Reporte No. {report_number}")

    img_izq = os.path.join("static", "users/image/tecnm.jfif")
    img_der = os.path.join("static", "users/image/ser.jfif")
    if os.path.exists(img_izq): c.drawImage(img_izq, 50, 700, width=75, height=75)
    if os.path.exists(img_der): c.drawImage(img_der, 500, 700, width=75, height=75)

    data_table = [
        ["No. de Control:", matricula],
        ["Nombre:", first_name],
        ["Apellido Paterno", middle_name],
        ["Apellido Materno", last_name]
    ]
    table = Table(data_table, colWidths=[100, 400])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("SPAN", (1, 1), (1, 1)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
    ]))
    table.wrapOn(c, 50, 610)
    table.drawOn(c, 50, 610)

    fecha_inicio = registro.fechaInicio
    periodo_letra = "A" if fecha_inicio.month <= 6 else "B" 
    
    periodo_data = [
        [f"Periodo Reportado: {periodo_letra}"],
        ["Del día:", fecha_inicio.day, "Mes", fecha_inicio.strftime("%B"), fecha_inicio.year],
        ["Al día:", registro.fechaDeFinalizacion.day, "Mes", registro.fechaDeFinalizacion.strftime("%B"), registro.fechaDeFinalizacion.year],
    ]
    periodo_table = Table(periodo_data, colWidths=[200, 50, 50, 100, 100])
    periodo_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("SPAN", (0, 0), (4, 0)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ]))
    periodo_table.wrapOn(c, 50, 520)
    periodo_table.drawOn(c, 50, 520)

    textos = [
        f"El presente documento certifica que el/la estudiante {first_name} {middle_name} {last_name}",
        f"De {semester}° semestre, con número de matrícula {matricula}",
        f"ha cumplido satisfactoriamente con las {total_horas['total'] or 0} horas de servicio social requeridas.",
        f"Para realizar el informe {report_number}°"
    ]
    for i, texto in enumerate(textos):
        c.drawString(50, 500-(i*15), texto)
        
    c.showPage()
    c.save() 

    buffer.seek(0)
    return buffer