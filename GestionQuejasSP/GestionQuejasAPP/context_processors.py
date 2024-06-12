from django.template import context_processors

from .models import Notificacion
from .forms import ReporteQuejasForm

# def notificaciones_sin_leer(request):
#     # Obtener el usuario actual
#     if request.user.is_authenticated:
#         usuario = request.user
#
#     # Obtener la cantidad de notificaciones sin leer
#         cantidad_notificaciones_sin_leer = Notificacion.objects.filter(usuario=usuario, leida=False).count()
#
#     # Retornar el contexto con la cantidad de notificaciones sin leer
#         return {'cantidad_notificaciones_sin_leer': cantidad_notificaciones_sin_leer}


class MyFormMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Crea una instancia del formulario que deseas agregar como contexto
        form = ReporteQuejasForm()

        # Agrega el formulario al contexto de la solicitud
        request.form = form

        response = self.get_response(request)

        return response

