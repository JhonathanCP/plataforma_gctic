from django.urls import path
from pbi.views import CustomUserListCreateView, CustomUserRetrieveUpdateDeleteView, SolicitudApproveDenyView, SolicitudRetrieveUpdateDeleteView,GrupoListCreateView, GrupoRetrieveUpdateDeleteView, ReporteListCreateView, ReporteRetrieveUpdateDestroyView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDeleteView.as_view(), name='user-retrieve-update-delete'),
    path('grupos/', GrupoListCreateView.as_view(), name='grupo-list-create'),
    path('grupos/<int:pk>/', GrupoRetrieveUpdateDeleteView.as_view(), name='grupo-retrieve-update-delete'),
    path('reportes/', ReporteListCreateView.as_view(), name='reporte-list-create'),
    path('reportes/<int:pk>/', ReporteRetrieveUpdateDestroyView.as_view(), name='reporte-retrieve-update-destroy'),
    path('solicitudes/', SolicitudRetrieveUpdateDeleteView.as_view(), name='solicitud-list-create'),
    path('solicitudes/<int:pk>/', SolicitudApproveDenyView.as_view(), name='solicitud-process'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
