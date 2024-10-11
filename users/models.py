from django.db import models

# Create your models here.
from django.db import models

class Usuario(models.Model):
    matricula = models.CharField(max_length=9, primary_key=True)
    password = models.CharField(max_length=10)
    nombre = models.CharField(max_length=10)
    apellidoM = models.CharField(max_length=10)
    apellidoP = models.CharField(max_length=10)

class RegistroAlServicioSocial(models.Model):
    idRegistro = models.AutoField(primary_key=True)  # Usar AutoField para incrementar automáticamente
    matricula = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField()
    fechaDeFinalizacion = models.DateTimeField()

class RegistroDiario(models.Model):
    idRegistroDiario = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField()
    horasDiaria = models.IntegerField()
