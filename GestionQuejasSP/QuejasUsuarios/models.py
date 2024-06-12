from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuejaU(models.Model):
    nombre_apellidos = models.CharField(max_length=50)
    asunto = models.CharField(max_length=100,default="")
    telefono = models.IntegerField(null=True,blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    fechaT = models.DateField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    argumento= models.TextField(max_length=10000,blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_apellidos


class DocumentoQU(models.Model):
    quejaU = models.ForeignKey(QuejaU, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='documentos/')

    def __str__(self):
        return self.archivo.name