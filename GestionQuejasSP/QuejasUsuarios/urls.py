from django.contrib import admin
from django.urls import path, include
from .views import listar_queja,eliminar_queja,ver_queja,ver_queja2
from .views import InsertarQuejaView,EditarQuejaView


urlpatterns = [
    path('insertar_quejaU/', InsertarQuejaView.as_view(), name="insertar_quejasU"),
    path('listar_quejaU/', listar_queja, name="listar_quejasU"),
    path('editar_quejasU/<int:pk>/', EditarQuejaView.as_view(), name="editar_quejasU"),
    path('eliminar_quejaU/<int:numero>/', eliminar_queja, name="eliminar_quejaU"),
    path('ver_detalles/<int:numero>/', ver_queja, name="ver_detalles"),
    path('ver_detalles2/<int:id>/', ver_queja2, name="ver_detalles2"),



]

