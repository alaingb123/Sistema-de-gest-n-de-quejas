from django.contrib import admin

from .models import Queja,Respuesta,EntidadAfectada,CasoPrensa,Conclusion,Clasificacion,Satisfaccion,Procedencia,Via,Modalidad,Notificacion
# Register your models here.

class Queja_Admin(admin.ModelAdmin):
    readonly_fields = ('created','updated')
admin.site.register(Queja,Queja_Admin)

class Notificacion_admin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion','queja_id')
admin.site.register(Notificacion,Notificacion_admin)

class Respuesta_Admin(admin.ModelAdmin):
    readonly_fields = ('created','updated')
admin.site.register(Respuesta,Respuesta_Admin)

class EntidadAfectada_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(EntidadAfectada,EntidadAfectada_Admin)

class CasoPrensa_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(CasoPrensa,CasoPrensa_Admin)

class Conculision_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(Conclusion,Conculision_Admin)

class Clasificacion_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(Clasificacion,Clasificacion_Admin)

class Satisfaccion_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(Satisfaccion,Satisfaccion_Admin)

class Procedencia_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(Procedencia,Procedencia_Admin)

class Via_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(Via,Via_Admin)

class Modalidad_Admin(admin.ModelAdmin):
    list_display = ('nombre',)  # campos que se mostrarán en la lista de objetos de EntidadAfectada
    search_fields = ('nombre',)  # campos por los que se podrá buscar en la lista de objetos de EntidadAfectada
admin.site.register(Modalidad,Modalidad_Admin)



from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GestionQuejasAPP'

    def ready(self):
        import GestionQuejasAPP.signals

