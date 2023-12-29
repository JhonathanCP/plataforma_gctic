from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import Permission, Group


class CustomUser(AbstractUser):
    # Agrega tus campos personalizados aquí
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    dni = models.CharField(max_length=9, null=True)
    telefono_contacto = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    sede = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)    
    
    # Otros campos personalizados que puedas necesitar
    def __str__(self):
        return self.username

class Solicitud(models.Model):
    # Campos personalizados para la solicitud
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    dni = models.CharField(max_length=9, unique=True)
    telefono_contacto = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    sede = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    motivo_solicitud = models.CharField(max_length=700, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    # Campo para el estado de la solicitud
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Solicitud de {self.nombres} {self.apellidos} de {self.sede} - {self.area}"

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    link = models.URLField(blank=True, null=True, max_length=400)
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, related_name='reportes', null=True)

    def __str__(self):
        return self.nombre
    
class PermisoGrupo(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    grupo = models.ForeignKey('pbi.Grupo', on_delete=models.CASCADE)
    # Otros campos específicos del permiso para grupos

class PermisoReporte(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reporte = models.ForeignKey('pbi.Reporte', on_delete=models.CASCADE)
    # Otros campos específicos del permiso para reportes