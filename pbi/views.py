from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Solicitud, Grupo, Reporte, PermisoGrupo, PermisoReporte
from .serializers import CustomUserSerializer, SolicitudSerializer, GrupoSerializer, ReporteSerializer, PermisoGrupoSerializer, PermisoReporteSerializer, AsignarPermisoGrupoSerializer, AsignarPermisoReporteSerializer
from django.forms.models import model_to_dict

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

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden asignar permisos a otros usuarios"}, status=status.HTTP_403_FORBIDDEN)

        usuario_id = serializer.validated_data['usuario_id']
        grupo_id = serializer.validated_data['grupo_id']

        # Crear el permiso de grupo para el usuario especificado
        PermisoGrupo.objects.create(usuario_id=usuario_id, grupo_id=grupo_id)

        return Response({"detail": "Permiso de grupo asignado correctamente"}, status=status.HTTP_201_CREATED)

class AsignarPermisoReporteView(generics.CreateAPIView):
    serializer_class = AsignarPermisoReporteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si el usuario autenticado es un superusuario
        if not request.user.is_superuser:
            return Response({"detail": "Solo los superusuarios pueden asignar permisos a otros usuarios"}, status=status.HTTP_403_FORBIDDEN)

        usuario_id = serializer.validated_data['usuario_id']
        reporte_id = serializer.validated_data['reporte_id']

        # Crear el permiso de reporte para el usuario especificado
        PermisoReporte.objects.create(usuario_id=usuario_id, reporte_id=reporte_id)

        return Response({"detail": "Permiso de reporte asignado correctamente"}, status=status.HTTP_201_CREATED)