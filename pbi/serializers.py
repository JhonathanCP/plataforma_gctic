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
    grupo_id = serializers.SerializerMethodField(read_only=True)
    grupo_nombre = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Reporte
        fields = ['id', 'nombre', 'fecha_creacion', 'descripcion', 'activo', 'link', 'grupo', 'grupo_id', 'grupo_nombre']
    def get_grupo_id(self, reporte):
        return reporte.grupo.id if reporte.grupo else None

    def get_grupo_nombre(self, reporte):
        return reporte.grupo.nombre if reporte.grupo else None
    
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
        reportes_permisos = PermisoReporte.objects.filter(usuario=user, reporte__grupo=instance)
        filtered_reportes = [
            ReporteSerializer(permiso.reporte).data for permiso in reportes_permisos
        ]

        # Actualizar la representación con los reportes filtrados
        representation['reportes'] = filtered_reportes

        return representation

class PermisoGrupoSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    grupo = serializers.SerializerMethodField()

    class Meta:
        model = PermisoGrupo
        fields = ['id', 'usuario', 'grupo']

    def get_grupo(self, permiso_grupo):
        grupo = permiso_grupo.grupo
        return {'id': grupo.id, 'nombre': grupo.nombre}

class PermisoReporteSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    reporte = serializers.SerializerMethodField()

    class Meta:
        model = PermisoReporte
        fields = ['id', 'usuario', 'reporte']

    def get_reporte(self, permiso_reporte):
        reporte = permiso_reporte.reporte
        return {'id': reporte.id, 'nombre': reporte.nombre}


class AsignarPermisoGrupoSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    grupo_id = serializers.IntegerField()

class AsignarPermisoReporteSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    reporte_id = serializers.IntegerField()

class QuitarPermisoGrupoSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    grupo_id = serializers.IntegerField()

class QuitarPermisoReporteSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    reporte_id = serializers.IntegerField()