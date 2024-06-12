from django.db.models.signals import post_migrate
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from GestionQuejasAPP.models import Respuesta,Queja,EntidadAfectada,Procedencia,Conclusion,Clasificacion,CasoPrensa,Satisfaccion,Via,Modalidad
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

def create_default_groups(sender, **kwargs):
    # Obtener los objetos de grupo
    jefe_dep_group, _ = Group.objects.get_or_create(name='JefeDep')
    funcionario_group, _ = Group.objects.get_or_create(name='Funcionario')
    moderador_group, _ = Group.objects.get_or_create(name='Moderador')

    # Obtener los permisos de Queja y Respuesta
    content_type = ContentType.objects.get_for_model(Queja)
    content_type2 = ContentType.objects.get_for_model(Respuesta)
    permissions = Permission.objects.filter(content_type=content_type)
    permissions2 = Permission.objects.filter(content_type=content_type2)

    # Agregar los permisos al grupo de funcionario y al grupo de JefeDep
    for permission in permissions:
        funcionario_group.permissions.add(permission)
        jefe_dep_group.permissions.add(permission)

    for permission in permissions2:
        funcionario_group.permissions.add(permission)
        jefe_dep_group.permissions.add(permission)


    # Obtener los content types de User y Group
    content_types = ContentType.objects.get_for_models(User, Group,EntidadAfectada,Procedencia,Conclusion,Clasificacion,CasoPrensa,Satisfaccion,Via,Modalidad).values()

    permissions = Permission.objects.filter(content_type__in=content_types)


    # Agregar los permisos al grupo de moderador
    for permission in permissions:
        moderador_group.permissions.add(permission)

    # Crear objetos EntidadAfectada si no existen
    entidades = ['1-Recursos humanos', '2-Higiene y epidemiología', '3-Asistencia médica','4-Vicedirección económica','5-Vicedirección general']
    for entidad in entidades:
        if not EntidadAfectada.objects.filter(nombre=entidad).exists():
            EntidadAfectada.objects.create(nombre=entidad)

    casos_de_prensas = ['1-No', '2-Plataforma bienestar', '3-Periodico granma']
    for caso in casos_de_prensas:
        if not CasoPrensa.objects.filter(nombre=caso).exists():
            CasoPrensa.objects.create(nombre=caso)

    conclusiones = ['1-Con razón', '2-Con razón en parte', '3-Sin razón']
    for conclusion in conclusiones:
        if not Conclusion.objects.filter(nombre=conclusion).exists():
            Conclusion.objects.create(nombre=conclusion)

    clasificaciones = ['1-Asistencia médica', '2-APS y enfermeria', '3-Por fallecimiento' ,'4-Higiene','5-Medicina óptica y audición','6-Asistencia social','7-Docencia','8-Laborales','9-Problemas administrativos','10-Ambulancia','11-Solicitud de RH y materiales','12-Construcción y mantenimiento','13-Tratos','14-Condiciones de trabajo','15-Vivienda','16-Salida del país','17-Otros']
    for clasificacion in clasificaciones:
        if not Clasificacion.objects.filter(nombre=clasificacion).exists():
            Clasificacion.objects.create(nombre=clasificacion)

    procedencias = ['1-MINSAP', '2-PCC', '3-APPP',
                       '4-Directo al sectorial', '5-Otros']
    for procedencia in procedencias:
        if not Procedencia.objects.filter(nombre=procedencia).exists():
            Procedencia.objects.create(nombre=procedencia)

    satisfacciones = ['1-Conforme', '2-Conforme en parte', '3-Inconforme']
    for satisfaccion in satisfacciones:
        if not Satisfaccion.objects.filter(nombre=satisfaccion).exists():
            Satisfaccion.objects.create(nombre=satisfaccion)

    vias = ['1-Carta', '2-Entrevista', '3-Teléfono', '4-Plataforma salud']
    for via in vias:
        if not Via.objects.filter(nombre=via).exists():
            Via.objects.create(nombre=via)

    modalidades = ['1-Solicitud', '2-Queja', '3-Anónimo o denuncia','4-Sugerencia','5-Reclamación','6-Reconocimiento']
    for modalidad in modalidades:
        if not Modalidad.objects.filter(nombre=modalidad).exists():
            Modalidad.objects.create(nombre=modalidad)

    groups = [
        {'name': '1-Recursos humanos'},
        {'name': '2-Higiene y epidemiología'},
        {'name': '3-Asistencia médica'},
        {'name': '4-Vicedirección económica'},
        {'name': '5-Vicedirección general'},
    ]

    for group in groups:
        group_obj, created = Group.objects.get_or_create(name=group['name'])


post_migrate.connect(create_default_groups, sender=apps.get_app_config('Usuario'))



