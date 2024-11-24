from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    matricula = models.CharField(max_length=9, primary_key=True)
    password = models.CharField(max_length=128)
    nombre = models.CharField(max_length=30)
    apellidoM = models.CharField(max_length=30, blank=True)
    apellidoP = models.CharField(max_length=30)
    semestre = models.CharField(max_length=1,default=1)
    
class RegistroAlServicioSocial(models.Model):
    idRegistro = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='registros_servicio_social')
    fechaInicio = models.DateTimeField()
    fechaDeFinalizacion = models.DateTimeField()

class RegistroDiario(models.Model):
    idRegistroDiario = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='registros_diarios')
    fecha = models.DateTimeField()
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True)  # Permite que sea nulo en la base de datos
    horasDiaria = models.IntegerField()
