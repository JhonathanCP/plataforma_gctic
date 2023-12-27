from rest_framework import serializers
from .models import CustomUser, Solicitud, Grupo, Reporte, PermisoGrupo, PermisoReporte

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nombres', 'apellidos', 'correo', 'dni', 'telefono_contacto', 'sede', 'area']

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'nombres', 'apellidos', 'correo', 'dni', 'telefono_contacto', 'sede', 'area', 'motivo_solicitud', 'fecha_creacion', 'estado']
        read_only_fields = ['id', 'fecha_creacion']

    def validate_correo(self, value):
        # Verificar que el correo pertenezca al dominio específico
        if not value.endswith('@essalud.gob.pe'):
            raise serializers.ValidationError("Solo se permiten correos con dominio @essalud.gob.pe.")
        return value

    def validate(self, data):
        estado = data.get('estado', '').lower()

        # Si el estado es "aprobado", no se requieren los campos específicos
        if estado == 'aprobado':
            return data

        # Validación estándar para otros estados
        for field in ['nombres', 'apellidos', 'correo', 'dni']:
            if not data.get(field):
                raise serializers.ValidationError({field: "Este campo es requerido."})

        return data

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id', 'nombre', 'fecha_creacion', 'descripcion', 'activo', 'link']

class GrupoSerializer(serializers.ModelSerializer):
    reportes = ReporteSerializer(many=True, read_only=True)

    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'fecha_creacion', 'descripcion', 'activo', 'reportes']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Obtener el usuario autenticado desde el contexto de la solicitud
        user = self.context['request'].user

        # Filtrar los reportes según los permisos del usuario
        reportes = representation['reportes']
        filtered_reportes = [reporte for reporte in reportes if user.has_perm('ver_reporte', reporte['id'])]

        # Actualizar la representación con los reportes filtrados
        representation['reportes'] = filtered_reportes

        return representation

class PermisoGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisoGrupo
        fields = '__all__'

class PermisoReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisoReporte
        fields = '__all__'

class AsignarPermisoGrupoSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    grupo_id = serializers.IntegerField()

class AsignarPermisoReporteSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    reporte_id = serializers.IntegerField()