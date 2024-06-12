from datetime import timedelta
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from multiupload.fields import MultiFileField
from django.contrib.postgres.fields import ArrayField

from QuejasUsuarios.models import QuejaU
from django.contrib.auth.models import User


# Create your models here.


#Campos seleccionables
class EntidadAfectada(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Modalidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Via(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Procedencia(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Clasificacion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class CasoPrensa(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre



class Queja(models.Model):
    numero = models.IntegerField(auto_created=True, default=1, editable=False)
    nombre_apellidos = models.CharField(max_length=50)
    entidadAfectada = models.ForeignKey(EntidadAfectada, on_delete=models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    via = models.ForeignKey(Via, on_delete=models.CASCADE)
    procedencia = models.ForeignKey(Procedencia, on_delete=models.CASCADE)
    clasificacion = models.ForeignKey(Clasificacion, on_delete=models.CASCADE)
    casoPrensa = models.ForeignKey(CasoPrensa, on_delete=models.CASCADE)
    fechaR = models.DateField()
    fechaT = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    orden = models.IntegerField(default=0)
    asunto = models.CharField(max_length=100, default="")
    argumento= models.TextField(max_length=10000,blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    queja_u = models.OneToOneField(QuejaU, on_delete=models.SET_NULL, null=True, blank=True, unique=True,related_name='queja_us')
    usuario_created = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='usuario_queja_created')
    usuario_update = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='usuario_queja_updated')
    no_procedece = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'queja'
        verbose_name_plural = 'quejas'

    def __str__(self):
        texto = 'numero: {}....Nombre y Apellidos: {}.... Fecha Recibido: {}'
        return texto.format(self.numero, self.nombre_apellidos, self.fechaR)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_number = Queja.objects.filter(fechaR__year=self.fechaR.year).order_by('-numero').first()
            if last_number:
                self.numero = last_number.numero + 1
            else:
                self.numero = 1
        super().save(*args, **kwargs)


class DocumentoQF(models.Model):
    queja = models.ForeignKey(Queja, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='documentos/')

    def __str__(self):
        return self.archivo.name


class Satisfaccion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Conclusion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Respuesta(models.Model):
    numero = models.OneToOneField(Queja, on_delete=models.CASCADE, related_name='respuesta')
    responsable = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=10000)
    entrega = models.BooleanField(default=False)
    satisfaccion = models.ForeignKey(Satisfaccion, on_delete=models.CASCADE,null=True)
    conclusion = models.ForeignKey(Conclusion, on_delete=models.CASCADE)
    fechaE = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    usuario_created = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='usuario_respuesta_created')
    usuario_update = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='usuario_respuesta_updated')

    class Meta:
        verbose_name = 'respuesta'
        verbose_name_plural = 'respuestas'

    def __str__(self):
        azucar = 'Queja: {} Responsable: {} Entrega: {} '
        return azucar.format(self.numero, self.responsable, self.entrega)



class DocumentoR(models.Model):
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='documentos/')

    def __str__(self):
        return self.archivo.name


@receiver(pre_save, sender=Queja)
def actualizar_fecha_termino(sender, instance, **kwargs):
    if instance.fechaR:
        instance.fechaT = instance.fechaR + timedelta(days=30)


from django.contrib.auth.models import User

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    queja_id=models.IntegerField(null=True)

    def __str__(self):
        return self.mensaje


class AnalisisQueja(models.Model):
    queja = models.OneToOneField(Queja, on_delete=models.CASCADE, related_name='analisis')
    analisis = models.TextField()
    fecha_analisis = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análisis de la Queja #{self.queja.nombre_apellidos}"

