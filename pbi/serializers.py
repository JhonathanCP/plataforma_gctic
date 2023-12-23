from rest_framework import serializers
from .models import CustomUser, Solicitud, Grupo, Reporte

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nombres', 'apellidos', 'correo', 'dni', 'telefono_contacto', 'sede', 'area']

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'nombres', 'apellidos', 'correo', 'dni', 'telefono_contacto', 'sede', 'area', 'motivo_solicitud', 'fecha_creacion', 'estado']
        read_only_fields = ['id', 'fecha_creacion']

    def validate(self, data):
        estado = data.get('estado', '').lower()

        # Si el estado es "aprobado", no se requieren los campos específicos
        if estado == 'aprobado':
            return data

        # Validación estándar para otros estados
        for field in ['nombres', 'apellidos', 'correo', 'dni']:
            if not data.get(field):
                raise serializers.ValidationError({field: "This field is required."})

        return data

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'fecha_creacion', 'descripcion', 'activo']

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id', 'nombre', 'fecha_creacion', 'descripcion', 'activo', 'link', 'grupo']