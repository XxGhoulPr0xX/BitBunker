from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from ..models import RegistroDiario

def getFechasPeriodoEscolar(periodo):
    año_actual = datetime.now().year
    if periodo == 'A':
        inicio = timezone.make_aware(datetime(año_actual, 1, 29))
        fin = timezone.make_aware(datetime(año_actual, 5, 31, 23, 59))
        return inicio, fin
    elif periodo == 'B':
        inicio = timezone.make_aware(datetime(año_actual, 8, 21))
        fin = timezone.make_aware(datetime(año_actual, 12, 8, 23, 59))
        return inicio, fin
    return None, None

def RegistrarHorasDiarias(usuario):
    tiempo_actual = timezone.localtime(timezone.now())
    fecha_hoy = tiempo_actual.date()
    if RegistroDiario.objects.filter(matricula=usuario, fecha=fecha_hoy).exists():
        total = RegistroDiario.objects.filter(matricula=usuario).aggregate(total=Sum('horasDiaria'))
        return False, total['total']

    hora_entrada = now()
    hora_salida = hora_entrada + timedelta(hours=4)
    
    RegistroDiario.objects.create(
        matricula=usuario,
        fecha=fecha_hoy,
        horaEntrada=hora_entrada,
        horaSalida=hora_salida,
        horasDiaria=4
    )
    
    total = RegistroDiario.objects.filter(matricula=usuario).aggregate(total=Sum('horasDiaria'))
    return True, total['total'] or 0