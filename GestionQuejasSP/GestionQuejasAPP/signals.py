from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
from .models import Queja,Notificacion,Respuesta
from QuejasUsuarios.models import QuejaU



@receiver(post_save, sender=Queja)
def nueva_queja(sender, instance, created, **kwargs):
    ultima_queja = instance



    if created:
        # Aquí puedes enviar la notificación de que se creó una nueva queja


        grupo = Group.objects.get(name=ultima_queja.entidadAfectada.nombre)  # Obtener el grupo específico
        usuarios = User.objects.filter(groups=grupo)  # Filtrar los usuarios por el grupo
        for usuario in usuarios:
            notificacion = Notificacion(usuario=usuario,
                                        mensaje='Se ha recibido una nueva queja para su departamento con el número: '+str(ultima_queja.numero),
                                        queja_id=ultima_queja.pk)
            notificacion.save()

        if ultima_queja.queja_u:
            fecha_formateada = ultima_queja.fechaT.strftime('%d/%m/%y')
            user =ultima_queja.queja_u.usuario
            notificacion = Notificacion(usuario=user,
                                        mensaje=ultima_queja.usuario_created.username + ' ha registrado su queja con el número: ' + str(
                                            ultima_queja.numero) + ' el departamento: ' + ultima_queja.entidadAfectada.nombre + ' debe darle respuestas antes de: '+ str (fecha_formateada),
                                        queja_id=ultima_queja.pk)
            notificacion.save()

    else:

        if  ultima_queja.usuario_update != None:
            if ultima_queja.no_procedece == False:
                user=ultima_queja.usuario_update.username

                grupo = Group.objects.get(name=ultima_queja.entidadAfectada.nombre)  # Obtener el grupo específico
                usuarios = User.objects.filter(groups=grupo)  # Filtrar los usuarios por el grupo
                for usuario in usuarios:
                    notificacion = Notificacion(usuario=usuario,
                                                mensaje=user +' ha modificado la queja con el número: ' + str(
                                                    ultima_queja.numero), queja_id=ultima_queja.pk)
                    notificacion.save()



@receiver(post_save, sender=Respuesta)
def respuesta_queja(sender, instance,created, **kwargs):


    ultima_respuesta=instance

    if created:

        user=ultima_respuesta.usuario_created.username

        grupo = Group.objects.get(name="Funcionario")  # Obtener el grupo específico

        usuarios = User.objects.filter(groups=grupo)  # Filtrar los usuarios por el grupo

        for usuario in usuarios:
            notificacion = Notificacion(usuario=usuario,
                                    mensaje=user + ' ha respondido la queja número: ' + str(
                                        ultima_respuesta.numero.numero) + ' del departamento: ' + ultima_respuesta.numero.entidadAfectada.nombre,
                                    queja_id=ultima_respuesta.numero.pk)
            notificacion.save()

        if ultima_respuesta.numero.queja_u:
            usuario = ultima_respuesta.numero.queja_u.usuario
            notificacion = Notificacion(usuario=usuario,
                                    mensaje=user + ' ha respondido su queja número: ' + str(
                                        ultima_respuesta.numero.numero) + ' del departamento: ' + ultima_respuesta.numero.entidadAfectada.nombre,
                                    queja_id=ultima_respuesta.numero.pk)
            notificacion.save()
    else:

        grupo = Group.objects.get(name="Funcionario")  # Obtener el grupo específico
        grupo2 = Group.objects.get(name=ultima_respuesta.numero.entidadAfectada.nombre)  # Obtener el grupo específico

        usuarios = User.objects.filter(groups=grupo).union(User.objects.filter(groups=grupo2))
        user=ultima_respuesta.usuario_update.username
        for usuario in usuarios:
            notificacion = Notificacion(usuario=usuario,
                                        mensaje=user +' ha modificado la respuesta : ' + str(
                                            ultima_respuesta.numero.numero) + ' del departamento: ' + ultima_respuesta.numero.entidadAfectada.nombre,
                                        queja_id=ultima_respuesta.numero.pk)
            notificacion.save()

        if ultima_respuesta.numero.queja_u:
            user = ultima_respuesta.numero.queja_u.usuario
            user_update = ultima_respuesta.usuario_update.username
            notificacion = Notificacion(usuario=user,
                                        mensaje=user_update + ' ha modificado la respuesta: ' + str(
                                            ultima_respuesta.numero.numero) + ' del departamento: ' + ultima_respuesta.numero.entidadAfectada.nombre,
                                        queja_id=ultima_respuesta.numero.pk)
            notificacion.save()


@receiver(post_save, sender=QuejaU)
def nueva_queja_u(sender, instance, created, **kwargs):

    if created:
        # Aquí puedes enviar la notificación de que se creó una nueva queja
        grupo = Group.objects.get(name="Funcionario")  # Obtener el grupo específico
        ultima_queja = instance

        usuarios = User.objects.filter(groups=grupo)

        for usuario in usuarios:
            notificacion = Notificacion(usuario=usuario,
                                    mensaje='Se ha recibido una nueva queja en la Plataforma Salud',
                                    queja_id=ultima_queja.pk)

            notificacion.save()













