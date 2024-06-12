

from django.db import models

from GestionQuejasAPP.models import EntidadAfectada
from QuejasUsuarios.models import QuejaU
from django.contrib.auth.models import User



class Usuario_Departamento(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='departamento')
    entidad = models.ForeignKey(EntidadAfectada, on_delete=models.CASCADE, related_name='departamento', null=True)

    def __str__(self):
        return self.user.username