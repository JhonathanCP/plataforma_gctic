from django.urls import path
from django.contrib import admin
from pbi.views import CustomUserListCreateView, CustomUserRetrieveUpdateDeleteView, SolicitudApproveDenyView, SolicitudRetrieveUpdateDeleteView,GrupoListCreateView, GrupoRetrieveUpdateDeleteView, ReporteListCreateView, ReporteRetrieveUpdateDestroyView, PermisoGrupoListCreateView, PermisoReporteListCreateView, AsignarPermisoGrupoView, AsignarPermisoReporteView, AsignarTodosLosPermisosView, QuitarPermisoGrupoView, QuitarPermisoReporteView, PermisosUsuarioView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDeleteView.as_view(), name='user-retrieve-update-delete'),
    path('grupos/', GrupoListCreateView.as_view(), name='grupo-list-create'),
    path('grupos/<int:pk>/', GrupoRetrieveUpdateDeleteView.as_view(), name='grupo-retrieve-update-delete'),
    path('reportes/', ReporteListCreateView.as_view(), name='reporte-list-create'),
    path('reportes/<int:pk>/', ReporteRetrieveUpdateDestroyView.as_view(), name='reporte-retrieve-update-destroy'),
    path('solicitudes/', SolicitudRetrieveUpdateDeleteView.as_view(), name='solicitud-list-create'),
    path('solicitudes/<int:pk>/', SolicitudApproveDenyView.as_view(), name='solicitud-process'),
    path('permisos/grupos/', PermisoGrupoListCreateView.as_view(), name='permiso-grupo-list-create'),
    path('permisos/reportes/', PermisoReporteListCreateView.as_view(), name='permiso-reporte-list-create'),
    path('permisos/grupos/asignar/', AsignarPermisoGrupoView.as_view(), name='asignar-permiso-grupo'),
    path('permisos/reportes/asignar/', AsignarPermisoReporteView.as_view(), name='asignar-permiso-reporte'),
    path('permisos/grupos/quitar/', QuitarPermisoGrupoView.as_view(), name='quitar-permiso-grupo'),
    path('permisos/reportes/quitar/', QuitarPermisoReporteView.as_view(), name='quitar-permiso-reporte'),
    path('permisos/todos/<int:usuario_id>/', AsignarTodosLosPermisosView.as_view(), name='asignar-todos-los-permisos'),
    path('permisos/usuario/<int:pk>/', PermisosUsuarioView.as_view(), name='permisos-usuario'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
