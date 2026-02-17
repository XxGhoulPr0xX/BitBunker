import json
from django.http import JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Usuario
from ..Services import GenerarPDF, RegistrarHorasDiarias

@csrf_exempt
def save_pdf(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            matricula = request.session.get('matricula')
            pdf_buffer = GenerarPDF(data, matricula)
            return FileResponse(
                pdf_buffer, 
                as_attachment=True, 
                filename=f"Reporte_{data.get('reportNumber', '1')}.pdf"
            )
        except Exception as e:
            print(f"Error generando PDF: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=404)

@csrf_exempt
def contador(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido."}, status=405)
    matricula = request.session.get('matricula')
    if not matricula:
        return JsonResponse({"error": "Sesión inválida."}, status=400)
    try:
        usuario = Usuario.objects.get(matricula=matricula)
        exito, horas_totales = RegistrarHorasDiarias(usuario)
        if exito:
            return JsonResponse({
                "message": "Horas registradas correctamente.",
                "horasTotales": horas_totales
            }, status=201)
        else:
            return JsonResponse({
                "error": "Ya existe un registro para hoy.", 
                "horasTotales": horas_totales
            }, status=400)
            
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado."}, status=404)