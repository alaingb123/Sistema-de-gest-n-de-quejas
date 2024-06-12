from django.contrib import admin

# Register your models here.
from .models import QuejaU
class QuejaU_Admin(admin.ModelAdmin):
    readonly_fields = ('created','updated')
admin.site.register(QuejaU,QuejaU_Admin)
