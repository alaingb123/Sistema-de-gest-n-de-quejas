from django.apps import AppConfig





class GestionquejasappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GestionQuejasAPP'

    def ready(self):
         import GestionQuejasAPP.signals





