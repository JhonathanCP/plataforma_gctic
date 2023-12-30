from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Solicitud, Grupo, Reporte, PermisoGrupo, PermisoReporte
from .serializers import CustomUserSerializer, SolicitudSerializer, GrupoSerializer, ReporteSerializer, PermisoGrupoSerializer, PermisoReporteSerializer, AsignarPermisoGrupoSerializer, AsignarPermisoReporteSerializer, QuitarPermisoGrupoSerializer, QuitarPermisoReporteSerializer
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

class CustomUserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

class SolicitudApproveDenyView(generics.UpdateAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        estado = request.data.get('estado', '').lower()

        if estado == 'aprobado':
            dni = instance.dni
            password = dni  # Puedes personalizar la lógica para generar una contraseña más segura
            correo_parts = instance.correo.split('@')
            username = correo_parts[0]

            # Crear el usuario y asignar la contraseña
            user_data = model_to_dict(instance)
            
            # Excluir los campos no necesarios
            user_data.pop('id', None)
            user_data.pop('motivo_solicitud', None)
            user_data.pop('fecha_creacion', None)
            user_data.pop('estado', None)

            CustomUser.objects.create_user(username=username, password=password, **user_data)

        # Actualizar el estado de la solicitud
        instance.estado = estado
        instance.save()

        return Response({"detail": f"Solicitud {estado}"}, status=status.HTTP_200_OK)

class SolicitudRetrieveUpdateDeleteView(generics.ListCreateAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [permissions.AllowAny]  # Permite acceso sin autenticación

class CambiarContrasenaView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        nueva_contrasena = request.data.get('nueva_contrasena', '')
        confirmar_contrasena = request.data.get('confirmar_contrasena', '')

        # Realizar la lógica para cambiar la contraseña según tus necesidades
        if nueva_contrasena and nueva_contrasena == confirmar_contrasena:
            user.set_password(nueva_contrasena)
            user.cambio_primera_contrasena = True
            user.save()
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Las contraseñas no coinciden"}, status=status.HTTP_400_BAD_REQUEST)

class GrupoListCreateView(generics.ListCreateAPIView):
    serializer_class = GrupoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

    def get_queryset(self):
        # Obtener el usuario autenticado
        usuario = self.request.user

        # Filtrar los grupos basándote en los permisos del usuario
        permisos_grupo = PermisoGrupo.objects.filter(usuario=usuario)
        grupos_permitidos = [permiso.grupo for permiso in permisos_grupo]

        return grupos_permitidos

class GrupoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

class ReporteListCreateView(generics.ListCreateAPIView):
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Obtener el usuario autenticado
        usuario = self.request.user

        # Filtrar los reportes basándote en los permisos del usuario
        permisos_reporte = PermisoReporte.objects.filter(usuario=usuario)
        reportes_permitidos = [permiso.reporte for permiso in permisos_reporte]

        return reportes_permitidos  # Requiere autenticación

class ReporteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

class PermisoGrupoListCreateView(generics.ListCreateAPIView):
    queryset = PermisoGrupo.objects.all()
    serializer_class = PermisoGrupoSerializer
    permission_classes = [IsAuthenticated]

class PermisoReporteListCreateView(generics.ListCreateAPIView):
    queryset = PermisoReporte.objects.all()
    serializer_class = PermisoReporteSerializer
    permission_classes = [IsAuthenticated]

class AsignarPermisoGrupoView(generics.CreateAPIView):
    serializer_class = AsignarPermisoGrupoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario_id = serializer.validated_data['usuario_id']
        grupo_id = serializer.validated_data['grupo_id']

        # Verificar si el permiso de grupo ya existe para el usuario y grupo especificados
        if PermisoGrupo.objects.filter(usuario_id=usuario_id, grupo_id=grupo_id).exists():
            return Response({"detail": "El permiso de grupo ya existe para este usuario y grupo"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden asignar permisos a otros usuarios"}, status=status.HTTP_403_FORBIDDEN)

        # Crear el permiso de grupo para el usuario especificado
        PermisoGrupo.objects.create(usuario_id=usuario_id, grupo_id=grupo_id)

        return Response({"detail": "Permiso de grupo asignado correctamente"}, status=status.HTTP_201_CREATED)

class AsignarPermisoReporteView(generics.CreateAPIView):
    serializer_class = AsignarPermisoReporteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario_id = serializer.validated_data['usuario_id']
        reporte_id = serializer.validated_data['reporte_id']

        # Verificar si el permiso de reporte ya existe para el usuario y reporte especificados
        if PermisoReporte.objects.filter(usuario_id=usuario_id, reporte_id=reporte_id).exists():
            return Response({"detail": "El permiso de reporte ya existe para este usuario y reporte"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden asignar permisos a otros usuarios"}, status=status.HTTP_403_FORBIDDEN)

        # Crear el permiso de reporte para el usuario especificado
        PermisoReporte.objects.create(usuario_id=usuario_id, reporte_id=reporte_id)

        return Response({"detail": "Permiso de reporte asignado correctamente"}, status=status.HTTP_201_CREATED)

class QuitarPermisoGrupoView(generics.CreateAPIView):
    serializer_class = QuitarPermisoGrupoSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden quitar permisos a otros usuarios"}, status=status.HTTP_403_FORBIDDEN)

        usuario_id = serializer.validated_data['usuario_id']
        grupo_id = serializer.validated_data['grupo_id']

        # Obtener el permiso de grupo y eliminarlo si existe
        permiso_grupo = PermisoGrupo.objects.filter(usuario_id=usuario_id, grupo_id=grupo_id).first()
        if permiso_grupo:
            permiso_grupo.delete()

        return Response({"detail": "Permiso de grupo quitado correctamente"}, status=status.HTTP_200_OK)

class QuitarPermisoReporteView(generics.CreateAPIView):
    serializer_class = QuitarPermisoReporteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden quitar permisos a otros usuarios"}, status=status.HTTP_403_FORBIDDEN)

        usuario_id = serializer.validated_data['usuario_id']
        reporte_id = serializer.validated_data['reporte_id']

        # Obtener el permiso de reporte y eliminarlo si existe
        permiso_reporte = PermisoReporte.objects.filter(usuario_id=usuario_id, reporte_id=reporte_id).first()
        if permiso_reporte:
            permiso_reporte.delete()

        return Response({"detail": "Permiso de reporte quitado correctamente"}, status=status.HTTP_200_OK)

class AsignarTodosLosPermisosView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Obtener el ID del usuario desde los parámetros de la solicitud
        usuario_id = kwargs.get('usuario_id')

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden asignar todos los permisos a otros usuarios"}, status=status.HTTP_403_FORBIDDEN)

        # Obtener el usuario por ID
        usuario = get_object_or_404(CustomUser, id=usuario_id)

        # Obtener todos los grupos y reportes
        todos_los_grupos = Grupo.objects.all()
        todos_los_reportes = Reporte.objects.all()

        # Asignar permisos de grupo al usuario
        for grupo in todos_los_grupos:
            # Verificar si el permiso ya existe
            if not PermisoGrupo.objects.filter(usuario=usuario, grupo=grupo).exists():
                PermisoGrupo.objects.create(usuario=usuario, grupo=grupo)

        # Asignar permisos de reporte al usuario
        for reporte in todos_los_reportes:
            # Verificar si el permiso ya existe
            if not PermisoReporte.objects.filter(usuario=usuario, reporte=reporte).exists():
                PermisoReporte.objects.create(usuario=usuario, reporte=reporte)

        return Response({"detail": "Todos los permisos asignados correctamente"}, status=status.HTTP_201_CREATED)
    
class PermisosUsuarioView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']

        # Verificar si el usuario existe
        try:
            usuario = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, status=404)

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden ver los permisos de un usuario"}, status=403)

        # Obtener permisos de grupos y reportes para el usuario
        permisos_grupos = PermisoGrupo.objects.filter(usuario=usuario)
        permisos_reportes = PermisoReporte.objects.filter(usuario=usuario)

        # Serializar los permisos
        serializer_grupos = PermisoGrupoSerializer(permisos_grupos, many=True)
        serializer_reportes = PermisoReporteSerializer(permisos_reportes, many=True)

        return Response({
            "permisos_grupos": serializer_grupos.data,
            "permisos_reportes": serializer_reportes.data
        }, status=200)