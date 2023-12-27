from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

content_type1 = ContentType.objects.get_for_model(Group)
content_type2 = ContentType.objects.get_for_model(Permission)

# Crear permisos para grupos
grupo_permisos = [
    Permission.objects.create(codename='ver_grupo', name='Puede ver el grupo', content_type= content_type1),
    # Agregar más permisos según sea necesario
]

# Crear permisos para reportes
reporte_permisos = [
    Permission.objects.create(codename='ver_reporte', name='Puede ver el reporte', content_type= content_type2),
    # Agregar más permisos según sea necesario
]

# Asignar permisos al grupo
grupo_permiso = Permission.objects.get(codename='ver_grupo')
reporte_permiso = Permission.objects.get(codename='ver_reporte')

# Crear un grupo y asignarle permisos
grupo, created = Group.objects.get_or_create(name='Grupo con permisos')
grupo.permissions.add(grupo_permiso, reporte_permiso)

print("Permisos y grupo creados exitosamente.")
