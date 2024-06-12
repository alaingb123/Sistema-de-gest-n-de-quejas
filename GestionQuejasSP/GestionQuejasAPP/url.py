from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from .views import dash, InsertarQueja, insertar_respuesta, ModificarQ, eliminar_ultima_queja, modificarR, \
    eliminarR, acercaDe, informe,InsertarQuejaR, \
    ver_queja,ver_notificaciones ,insertar_respuesta_directa, eliminar_todas_las_notificaciones,\
    no_procede,procede,Comprobacion,Generar_reporte_de_quejas_del_mes,analisis_queja,editar_analisis_queja
import random
import string
from django.urls import path
from .views import eliminar_ultima_queja,obtener_nombre_usuario

# Generar un nombre de URL aleatorio
def generar_nombre_url():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=10))

urlpatterns = [
    path('', login_required(dash), name="dash"),
    # Gestionar Queja
    path('insertar_queja/', InsertarQueja.as_view(), name="insertar_queja"),
    path('modificarQ/<int:pk>/', ModificarQ.as_view(), name='modificarQ_with_numero'),
    path(generar_nombre_url() + '/<int:pk>/', eliminar_ultima_queja, name='eliminar_ultima_queja'),
    path('comprobacion/<int:numero>/', Comprobacion, name='comprobacion'),
    # Gestionar Respuesta
    path('insertar_respuesta/', insertar_respuesta, name='insertar_respuesta'),
    path('modificarR/<int:numero>/', modificarR, name="modificarR"),
    path('eliminarR/<int:numero>/', eliminarR, name="eliminarR"),

    # Acerca De
    path('acercaDe/', acercaDe, name="acercaDe"),


    path('informe/', informe, name="informe"),
    path('insertar_quejaR/<int:id>/', InsertarQuejaR, name="insertar_quejaR"),

    path('insertar_quejaR/<int:id>/', InsertarQuejaR, name="insertar_quejaR"),

    path('insertar_respuesta_directa/<int:id>/', insertar_respuesta_directa, name="insertar_respuesta_directa"),


    path('ver_queja/<int:numero>/', ver_queja, name="ver_queja"),



    path('notificacion/', ver_notificaciones, name="ver_notificacion"),
    path('eliminar_todas_notificaciones/', eliminar_todas_las_notificaciones, name="eliminar_todas_notificaciones"),

    path('no_procede/<int:pk>/', no_procede, name="no_procede"),
    path('procede/<int:pk>/', procede, name="procede"),

    path('reporte_de_quejas/', Generar_reporte_de_quejas_del_mes, name="reporte_de_quejas"),

    path('analisis/<int:queja_id>/', analisis_queja, name="analisis"),
    path('edit_analisis/<int:analisisqueja_id>/', editar_analisis_queja, name="edit_analisis"),




]

