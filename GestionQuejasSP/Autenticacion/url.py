from Autenticacion import views
from django.urls import path

from .views import logear, cerrar_sesion,create_user

urlpatterns = [

    path('', logear, name="autenticacion"),
    path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
    path('crear_usuario', create_user, name="creater"),

]