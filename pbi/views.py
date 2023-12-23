from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Solicitud, Grupo, Reporte
from .serializers import CustomUserSerializer, SolicitudSerializer, GrupoSerializer, ReporteSerializer
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

            # Crear el usuario y asignar la contraseña
            user_data = model_to_dict(instance)
            
            # Excluir los campos no necesarios
            user_data.pop('id', None)
            user_data.pop('motivo_solicitud', None)
            user_data.pop('fecha_creacion', None)
            user_data.pop('estado', None)

            CustomUser.objects.create_user(username=dni, password=password, **user_data)

        # Actualizar el estado de la solicitud
        instance.estado = estado
        instance.save()

        return Response({"detail": f"Solicitud {estado}"}, status=status.HTTP_200_OK)

class SolicitudRetrieveUpdateDeleteView(generics.ListCreateAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [permissions.AllowAny]  # Permite acceso sin autenticación

class GrupoListCreateView(generics.ListCreateAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

class GrupoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

class ReporteListCreateView(generics.ListCreateAPIView):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

class ReporteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación