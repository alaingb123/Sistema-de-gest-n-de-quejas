import base64
import json
from datetime import datetime
from urllib.parse import urljoin

from django.conf.urls.static import static
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth, TruncMonth
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import TemplateView
from io import BytesIO
from django.views.decorators.cache import never_cache

from GestionQuejasSP import settings
from .forms import QuejaForm, RespuestaForm, FiltroQuejasForm, ModificarRespuestaForm, FormMeses, AnalisisQuejaForm
from .models import Queja, Respuesta, DocumentoQF, DocumentoR, AnalisisQueja
from django.shortcuts import render
from django.db.models import Count, Case, When, IntegerField
from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat
from django.utils import timezone
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Queja,Respuesta,EntidadAfectada,CasoPrensa,Conclusion,Clasificacion,Satisfaccion,Procedencia,Via,Modalidad,Notificacion
from .forms import ReporteQuejasForm




Contraseña="Salud*19"

yearG=datetime.now().year;

@never_cache
@login_required
def dash(request):
    formR = ReporteQuejasForm()

    grupos = request.user.groups.values_list('name', flat=True)
    if 'Moderador' in grupos:
        return HttpResponseRedirect(reverse_lazy('user_list'))

    grupos = request.user.groups
    if not grupos.exists():
        return HttpResponseRedirect(reverse_lazy('listar_quejasU'))



    anos = Queja.objects.dates('fechaR', 'year').distinct()


    years = [anno.year for anno in anos]
    anos=years

    entidades = EntidadAfectada.objects.all()
    entida=request.GET.get('entidad')
    modalidad=request.GET.get('modalidad')
    via=request.GET.get('via')

    procedencia=request.GET.get('procedencia')
    casoPrensa = request.GET.get('casoPrensa')
    atrasada = request.GET.get('atrasada')


    clasificacion=request.GET.get('clasificacion')


    numero=request.GET.get('numero')
    nombre=request.GET.get('nombre_apellidos')


    # Obtener el año actual
    current_year = datetime.now().year
    now = datetime.now()
    now = now.date()
    # Obtener el valor del campo years del formulario
    year = request.GET.get('years', current_year)


    global yearG
    yearG=year



    # Filtrar las quejas por el año seleccionado en el formulario y ordenarlas por el campo de ordenamiento
    quejas = Queja.objects.filter(fechaR__year=year).order_by('orden')

    # Inicializar el formulario con el valor seleccionado en el formulario
    form = FiltroQuejasForm(initial={'years': year})


    grupos=request.user.groups.all()
    nombresE=[]
    for enti in entidades:
        nombresE.append(enti.nombre)

    for grupo in grupos:
        if grupo.name in nombresE:
            index = list(nombresE).index(grupo.name)
            e=entidades[index]
            quejas=quejas.filter(entidadAfectada=e)
            quejas=quejas.filter(no_procedece=False)



    if entida:
        quejas=quejas.filter(entidadAfectada=entida)
        entida = int(entida)

    if modalidad:
        quejas = quejas.filter(modalidad=modalidad)
        modalidad = int(modalidad)

    if via:
        quejas = quejas.filter(via=via)
        via = int(via)

    if procedencia:
        quejas = quejas.filter(procedencia=procedencia)
        procedencia = int(procedencia)

    if clasificacion:
        quejas = quejas.filter(clasificacion=clasificacion)
        clasificacion = int(clasificacion)

    if casoPrensa:
        quejas = quejas.filter(casoPrensa=casoPrensa)
        casoPrensa = int(casoPrensa)

    if numero:
        quejas = quejas.filter(numero=numero)

    if nombre:
        quejas = quejas.filter(nombre_apellidos__icontains=nombre)

    if request.method == 'GET':
        meses = FormMeses(request.GET)
        if meses.is_valid():
            mes = meses.cleaned_data['mes']
            dia = meses.cleaned_data['dias']
            # Aquí puedes procesar los datos enviados por el usuario
            if mes:
                quejas=quejas.filter(fechaR__month=mes)
            if dia:
                quejas=quejas.filter(fechaR__day=dia)
    else:
        meses = FormMeses()

    today = datetime.today().strftime('%Y-%m-%d')



    if 'atrasada' in request.GET:
        quejas = quejas.filter(fechaT__lt=today, respuesta__isnull=True)

    quejas = quejas.order_by('numero')


    ultima_queja = quejas.last()


    # Crear un objeto Paginator con las quejas y la cantidad de elementos por página
    paginator = Paginator(quejas, 20)

    # Obtener el número de página actual
    page_number = request.GET.get('page')
    page="page="+str(page_number)

    # Obtener la página correspondiente al número de página actual
    page_obj = paginator.get_page(page_number)

    search_params = request.GET.copy()
    search_params = search_params.urlencode()

    if page in search_params:
        search_params = search_params.replace(page, "")

    modalidades=Modalidad.objects.all()
    vias=Via.objects.all()
    procedencias=Procedencia.objects.all()
    casosPrensas=CasoPrensa.objects.all()

    clasificaciones = Clasificacion.objects.all()

    cantidad=quejas.count()

    year=int(year)

    context = {
        'form': form,
        'page_obj': page_obj, # Página actual
        'year': year,
        'entidades':entidades,
        'modalidades':modalidades,
        'vias':vias,
        'procedencias':procedencias,
        'clasificaciones':clasificaciones,
        'casosPrensas': casosPrensas,

        'entida':entida,
        'modalidad':modalidad,
        'via':via,
        'procedencia':procedencia,
        'clasificacion':clasificacion,
        'casoPrensa':casoPrensa,
        'meses':meses,
        'atrasada':atrasada,
        'search_params':search_params,
        'cantidad':cantidad,
        'ultima_queja':ultima_queja,
        'anos':anos,
        'dia':dia,
        'mes':mes,
        'now':now,
        'formR':formR

    }





    # Renderizar la plantilla y devolver una respuesta HttpResponse que contenga el objeto de contexto
    return render(request, 'dashboard/dash.html', context)



from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists()), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class InsertarQueja(CreateView):
    model = Queja
    form_class = QuejaForm

    template_name = 'Gestionar Queja/insertarQ.html'
    success_url = reverse_lazy('dash')

    def form_valid(self, form):
        queja = form.save(commit=False)
        queja.orden = Queja.objects.count() + 1
        queja.usuario_created = self.request.user
        queja.save()
        documentos = self.request.FILES.getlist('documento')
        for archivo in documentos:
            DocumentoQF.objects.create(queja=queja, archivo=archivo)
        return super().form_valid(form)


    def form_invalid(self, form):
        error_message = 'El formulario contiene los siguientes errores:<br>'
        for field, errors in form.errors.items():
            error_message += f'- {field}: {", ".join(errors)}<br>'
        return self.render_to_response(self.get_context_data(form=form, error_message=error_message))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entidades = EntidadAfectada.objects.all()
        casoPrensa = CasoPrensa.objects.all()
        clasificacion = Clasificacion.objects.all()
        procedencia = Procedencia.objects.all()
        via = Via.objects.all()
        modalidad = Modalidad.objects.all()
        context.update({
            'entidades': entidades,
            'casoPrensa': casoPrensa,
            'clasificacion': clasificacion,
            'procedencia': procedencia,
            'via': via,
            'modalidad': modalidad,
        })
        return context

from QuejasUsuarios.models import QuejaU
@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists())
def InsertarQuejaR(request,id):
    entidades = EntidadAfectada.objects.all()
    casoPrensa = CasoPrensa.objects.all()
    clasificacion = Clasificacion.objects.all()
    procedencia = Procedencia.objects.all()
    via = Via.objects.all()
    modalidad = Modalidad.objects.all()
    quejaU = get_object_or_404(QuejaU, id=id)
    context = {
        'entidades': entidades,
        'casoPrensa': casoPrensa,
        'clasificacion': clasificacion,
        'procedencia': procedencia,
        'via': via,
        'modalidad': modalidad,
        'quejaU': quejaU,
    }



    if request.method == 'POST':
        form = QuejaForm(request.POST, request.FILES)
        context = {
            'entidades': entidades,
            'casoPrensa': casoPrensa,
            'clasificacion': clasificacion,
            'procedencia': procedencia,
            'via': via,
            'modalidad': modalidad,
            'form': form,
        }
        if form.is_valid():
            # Procesar el formulario si los datos son válidos

            queja = form.save(commit=False)
            queja.orden = Queja.objects.count() + 1
            queja.queja_u =quejaU
            queja.usuario_created=request.user
            queja.save()
            # El formulario es válido, guardar los datos en la base de datos
            return HttpResponseRedirect(reverse_lazy('dash'))
        else:
            # Si los datos no son válidos, recopilar los mensajes de error del formulario
            error_message = 'El formulario contiene los siguientes errores:<br>'
            for field, errors in form.errors.items():
                error_message += f'- {field}: {", ".join(errors)}<br>'
    else:
        form = QuejaForm()
        context = {
            'entidades': entidades,
            'casoPrensa': casoPrensa,
            'clasificacion': clasificacion,
            'procedencia': procedencia,
            'via': via,
            'modalidad': modalidad,
            'form': form,
            'quejaU': quejaU,
        }

    return render(request, 'Gestionar Queja/insertarQ.html', {'entidades': entidades,
            'casoPrensa': casoPrensa,
            'clasificacion': clasificacion,
            'procedencia': procedencia,
            'via': via,
            'modalidad': modalidad,
            'form': form,
            'quejaU': quejaU,})


@method_decorator(never_cache, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists()), name='dispatch')
class ModificarQ(UpdateView):
    model = Queja
    form_class = QuejaForm
    template_name = 'Gestionar Queja/editarQueja.html'
    success_url = '/dash/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entidades'] = EntidadAfectada.objects.all()
        context['casoPrensa'] = CasoPrensa.objects.all()
        context['clasificacion'] = Clasificacion.objects.all()
        context['procedencia'] = Procedencia.objects.all()
        context['via'] = Via.objects.all()
        context['modalidad'] = Modalidad.objects.all()
        return context

    def get_initial(self):
        initial = super().get_initial()
        queja = self.get_object()
        initial['entidades'] = queja.entidadAfectada
        initial['casoPrensa'] = queja.casoPrensa
        initial['clasificacion'] = queja.clasificacion
        initial['procedencia'] = queja.procedencia
        initial['via'] = queja.via
        initial['modalidad'] = queja.modalidad
        return initial

    def form_valid(self, form):
        queja_vieja = self.get_object()
        for docu in queja_vieja.documentos.all():
            docu.delete()
        queja = form.save(commit=False)
        queja.usuario_update = self.request.user
        queja.save()

        documentos = self.request.FILES.getlist('documento')
        for archivo in documentos:
            DocumentoQF.objects.create(queja=queja, archivo=archivo)
        return super().form_valid(form)

@user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists())
def Comprobacion(request, numero):
    if request.method == 'POST':
        password = request.POST.get('passwordInput')


        # Verificar la contraseña aquí
        if password == Contraseña:
            url = reverse('eliminar_ultima_queja', args=[numero])
            return redirect(url)
        else:
            # Contraseña incorrecta, mostrar un mensaje de error
            messages.error(request, 'Contraseña incorrecta')
            return redirect('dash')

    return render(request, 'ComprobacionContrasM.html')






@user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists())
def eliminar_ultima_queja(request,pk):
    queja = get_object_or_404(Queja, id=pk)

    if request.method == 'POST':
        if queja:
            queja.delete()
            messages.success(request, 'La queja ha sido eliminada.')
        return redirect('dash')

    context = {
        'queja': queja
    }
    return render(request, 'eliminarQueja.html', context)


# Gestionar Respuesta
@never_cache
@user_passes_test(lambda u: u.groups.filter(name='JefeDep').exists())
def insertar_respuesta(request):

    satisfaccion = Satisfaccion.objects.all()
    conclusion = Conclusion.objects.all()
    entidades=EntidadAfectada.objects.all()
    error_message=""

    from .views import yearG

    # Obtener los grupos del usuario autenticado
    grupos = request.user.groups.all()

    # Filtrar las quejas sin respuesta y por año
    quejas = Queja.objects.filter(respuesta__isnull=True, fechaR__year=yearG)

    for grupo in grupos:
        # Obtener el nombre del grupo
        nombre_grupo = grupo.name
        for enti in entidades:
            if nombre_grupo==enti.nombre:
                quejas=quejas.filter(entidadAfectada=enti.id)

    if request.method == 'POST':
        form = RespuestaForm(request.POST, request.FILES)

        if form.is_valid():
            # Guardar la respuesta nueva
            respuesta = form.save(commit=False)
            respuesta.usuario_created=request.user
            respuesta.save()
            documentos = request.FILES.getlist('documento')
            for archivo in documentos:
                DocumentoR.objects.create(respuesta=respuesta, archivo=archivo)
            return redirect('dash')
        else:
            # Si los datos no son válidos, recopilar los mensajes de error del formulario
            error_message = 'El formulario contiene los siguientes errores:<br>'
            for field, errors in form.errors.items():
                error_message += f'- {field}: {", ".join(errors)}<br>'
    else:
        form = RespuestaForm()



    context = {
        'quejas': quejas,
        'form': form,
        'satisfaccion': satisfaccion,
        'conclusion': conclusion,
        'error_message':error_message,
    }
    return render(request, 'Gestionar Respuesta/insertarRespuesta.html',{'context': context})


@never_cache
@user_passes_test(lambda u: u.groups.filter(name='JefeDep').exists())
def insertar_respuesta_directa(request,id):

    satisfaccion = Satisfaccion.objects.all()
    conclusion = Conclusion.objects.all()
    entidades=EntidadAfectada.objects.all()
    error_message=""

    from .views import yearG

    grupos = request.user.groups.all()

    queja = get_object_or_404(Queja, id=id)

    entidad = queja.entidadAfectada.nombre

    grups = []

    for group in grupos:
        grups.append(group.name)

    if entidad in grups:
        print("La entidad está presente en el nombre del grupo")
    else:
        messages.warning(request, 'No posee los permisos necesarios para acceder a esa queja')
        return redirect('dash')

    if request.method == 'POST':
        form = RespuestaForm(request.POST, request.FILES)

        if form.is_valid():
            # Guardar la respuesta nueva
            respuesta = form.save(commit=False)
            respuesta.usuario_created=request.user
            respuesta.save()
            documentos = request.FILES.getlist('documento')
            for archivo in documentos:
                DocumentoR.objects.create(respuesta=respuesta, archivo=archivo)
            return redirect('dash')
        else:
            # Si los datos no son válidos, recopilar los mensajes de error del formulario
            error_message = 'El formulario contiene los siguientes errores:<br>'
            for field, errors in form.errors.items():
                error_message += f'- {field}: {", ".join(errors)}<br>'
    else:
        form = RespuestaForm()


    context = {
        'queja': queja,
        'form': form,
        'satisfaccion': satisfaccion,
        'conclusion': conclusion,
        'error_message':error_message,
    }

    return render(request, 'Gestionar Respuesta/insertar_respuesta_directa.html',{'context': context})

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='JefeDep').exists())
def modificarR(request, numero):
    # entidades = EntidadAfectada.objects.all()
    satisfaccion = Satisfaccion.objects.all()
    conclusion = Conclusion.objects.all()
    context = {
        'satisfaccion': satisfaccion,
        'conclusion': conclusion,
    }

    grupos = request.user.groups.all()


    queja = get_object_or_404(Queja, id=numero)
    entidad=queja.entidadAfectada.nombre

    grups = []

    for group in grupos:
        grups.append(group.name)


    if entidad in grups:
        print("La entidad está presente en el nombre del grupo")
    else:
        print("La entidad no está presente en el nombre del grupo")
        messages.warning(request, 'No posee los permisos necesarios para acceder a esa queja')
        return redirect('dash')

    respuesta = get_object_or_404(Respuesta, numero_id=numero)
    if request.method == 'POST':
        form = ModificarRespuestaForm(request.POST, request.FILES, instance=respuesta)
        if form.is_valid():
            respuesta1=form.save(commit=False)
            respuesta1.usuario_update=request.user
            respuesta1.save()
            for docu in respuesta.documentos.all():
                docu.delete()
            documentos = request.FILES.getlist('documento')
            for archivo in documentos:
                DocumentoR.objects.create(respuesta=respuesta1, archivo=archivo)
            return redirect('dash')
        else:
            # Agregar mensajes de error a la variable 'messages'
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RespuestaForm(instance=respuesta)
    return render(request, 'Gestionar Respuesta/modificarRespuesta.html', {'form': form, 'respuesta': respuesta , 'context' : context})

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='JefeDep').exists())
def eliminarR(request, numero):
    # Buscamos la respuesta por su número
    respuesta = get_object_or_404(Respuesta, numero=numero)

    if request.method == 'POST':
        # Si se ha enviado el formulario de confirmación, eliminamos la respuesta
        respuesta.delete()
        # Redirigimos a otra página, por ejemplo la lista de quejas
        return redirect('dash')

    return render(request, 'dashboard/eliminarR.html', {'respuesta': respuesta})



@never_cache
@login_required
def acercaDe(request):
    return render(request, 'acerca de.html')



@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists())
def informe(request):
    procedencia = request.GET.get('procedencia')
    clasificacion = request.GET.get('clasificacion')
    casoPrensa = request.GET.get('casoPrensa')
    atrasada = request.GET.get('atrasada')
    today = datetime.today().strftime('%Y-%m-%d')

    modalidades = ['1-Solicitud', '2-Queja', '3-Anonimo o Denuncia', '5-Reclamacion']

    from .views import yearG
    # Obtener la lista de entidades afectadas y meses únicos
    quejas=Queja.objects.filter(fechaR__year=yearG,modalidad__nombre__in=modalidades)



    if clasificacion:
        quejas=quejas.filter(clasificacion=clasificacion)
        clasificacion=int(clasificacion)


    if procedencia:
        quejas=quejas.filter(procedencia=procedencia)
        procedencia=int(procedencia)

    if casoPrensa:
        quejas=quejas.filter(casoPrensa=casoPrensa)
        procedencia = int(casoPrensa)




    if 'atrasada' in request.GET:
        quejas = quejas.filter(fechaT__lt=today, respuesta__isnull=True)

    quejas = quejas.filter(no_procedece=False)



    entidades = Queja.objects.values_list('entidadAfectada', flat=True).distinct().order_by('entidadAfectada')
    meses = quejas.annotate(mes=TruncMonth('fechaR')).values_list('mes', flat=True).distinct().order_by('mes')

    # Crear una matriz para los valores de la gráfica
    valores = []
    for mes in meses:
        fila = [0] * len(entidades)
        for i, entidad in enumerate(entidades):
            quejas = Queja.objects.filter(fechaR__month=mes.month,modalidad__nombre__in=modalidades, fechaR__year=mes.year, entidadAfectada=entidad)
            if clasificacion:
                quejas = quejas.filter(clasificacion=clasificacion)
                clasificacion = int(clasificacion)

            if procedencia:
                quejas = quejas.filter(procedencia=procedencia)
                procedencia = int(procedencia)

            if casoPrensa:
                quejas = quejas.filter(casoPrensa=casoPrensa)
                procedencia = int(casoPrensa)

            if 'atrasada' in request.GET:
                quejas = quejas.filter(fechaT__lt=today, respuesta__isnull=True)

            quejas = quejas.filter(no_procedece=False)

            cantidad = quejas.count()
            fila[i] = cantidad
        valores.append(fila)

    entidades = EntidadAfectada.objects.all()

    procedencias = Procedencia.objects.all()
    clasificaciones = Clasificacion.objects.all()
    casosPrensas = CasoPrensa.objects.all()


    # Pasar los datos a la plantilla
    return render(request, 'Gestionar Queja/resumen.html', {
        'entidades': entidades,
        'meses': meses,
        'valores': valores,
        'atrasada': atrasada,
        'casoPrensa': casoPrensa,
        'procedencia': procedencia,
        'procedencias': procedencias,
        'casosPrensas': casosPrensas,
        'clasificacion': clasificacion,
        'clasificaciones': clasificaciones,
    })

from django.http import Http404
from django.contrib.staticfiles.storage import staticfiles_storage
@login_required
def ver_queja(request, numero):
    try:
        queja = Queja.objects.get(pk=numero)

    except Queja.DoesNotExist:
        raise Http404("La queja no existe")  # Puedes personalizar el mensaje de error si lo deseas
    return render(request, 'Gestionar Queja/ver_queja.html', {'queja': queja})



@login_required
def eliminar_todas_las_notificaciones(request):
    Notificacion.objects.filter(usuario=request.user).delete()
    return redirect("ver_notificacion")



@login_required
def ver_notificaciones(request):
    if request.method == "POST":
        accion = request.POST.get("accion")


        if accion == "eliminar":
            notificaciones_seleccionadas = request.POST.getlist("notificaciones[]")
            Notificacion.objects.filter(id__in=notificaciones_seleccionadas).delete()

        return redirect("ver_notificacion")
    usuario = request.user
    notificaciones = Notificacion.objects.filter(usuario=usuario)
    notificaciones= sorted(notificaciones, key=lambda n: n.fecha_creacion, reverse=True)

    # Crear un objeto Paginator con las quejas y la cantidad de elementos por página
    paginator = Paginator(notificaciones, 10)

    # Obtener el número de página actual
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for notificacion in page_obj:
        notificacion.leida=True
        notificacion.save()



    return render(request, 'ver_notificaciones.html', {
        'notificaciones': notificaciones,
        'page_obj': page_obj,
    })




@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists())
def no_procede(request, pk):
    queja = get_object_or_404(Queja, pk=pk)
    queja.no_procedece=True
    queja.save()
    return redirect('dash')


@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Funcionario').exists())
def procede(request, pk):
    queja = get_object_or_404(Queja, pk=pk)
    queja.no_procedece=False
    queja.save()
    return redirect('dash')



@login_required
def obtener_nombre_usuario(request):
    nombre_usuario = request.user.username
    return nombre_usuario

@login_required
def Generar_reporte_de_quejas_del_mes(request):
    entidades = EntidadAfectada.objects.all()
    formA = AnalisisQuejaForm(request.POST)
    if request.method == 'POST':

        form = ReporteQuejasForm(request.POST)
        if form.is_valid():

            year = form.cleaned_data['years']
            month = form.cleaned_data['month']
            modalidades = ['1-Solicitud', '2-Queja', '3-Anonimo o Denuncia','5-Reclamacion']
            quejas = Queja.objects.filter(fechaR__year=year, fechaR__month=month,modalidad__nombre__in=modalidades)
            quejas = quejas.filter(no_procedece=False)
            informeT = quejas_informe(quejas)

            informe_entidades = []  # Lista para almacenar los informes de cada entidad

            for entidad in entidades:
                quejas_entidad = quejas.filter(entidadAfectada=entidad)  # Filtrar las quejas por entidad
                informe_entidad = quejas_informe(quejas_entidad)  # Obtener el informe para la entidad


                # Agregar el informe de la entidad a la lista
                informe_entidades.append({
                    'entidad': entidad,
                    'informe': informe_entidad
                })




            return render(request, 'Gestionar Queja/reporte_de_quejas.html', {
                'informeT': informeT,
                'informe_entidades': informe_entidades,
                'mes': month,
                'year': year,
                'formA': formA,
            })

        else:
            print(form.errors)



    return redirect('dash')


def quejas_informe(quejas):
    total_quejas = quejas.count()
    now = datetime.now()
    now = now.date()
    atrasada = 0
    asignada = 0
    inconforme = 0
    entregada = 0
    respondida = 0
    con_respuesta = 0
    lista_quejas_atrasadas = []
    lista_quejas_inconformes = []
    for queja in quejas:
        try:
            if queja.respuesta:
                if queja.respuesta.entrega == True:
                    entregada = entregada + 1
                    con_respuesta = con_respuesta + 1
                    if queja.respuesta.satisfaccion.nombre == '3-Inconforme':
                        inconforme = inconforme + 1
                        lista_quejas_inconformes.append(queja)

                else:
                    respondida = respondida + 1
                    con_respuesta = con_respuesta+1
        except:
            if queja.fechaT < now:
                atrasada = atrasada + 1
                lista_quejas_atrasadas.append(queja)
            else:
                asignada = asignada + 1





    informe = {
        'total_quejas': total_quejas,
        'entregada': entregada,
        'respondida': respondida,
        'atrasada': atrasada,
        'asignada': asignada,
        'inconforme': inconforme,
        'con_respuesta': con_respuesta,
        'lista_quejas_atrasadas': lista_quejas_atrasadas,
        'lista_quejas_inconformes': lista_quejas_inconformes
    }

    return informe


def analisis_queja(request,queja_id):
    q = get_object_or_404(Queja, pk=queja_id)
    if request.method == 'POST':
        form = AnalisisQuejaForm(request.POST)
        if form.is_valid():
            analisis_queja = form.save(commit=False)
            analisis_queja.queja = q
            # Aquí puedes realizar cualquier lógica adicional antes de guardar el objeto
            analisis_queja.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = AnalisisQuejaForm()

    return render(request, 'Gestionar Queja/agregar_motivo.html', {'form': form, 'queja':q})


def editar_analisis_queja(request, analisisqueja_id):
    analisisqueja = get_object_or_404(AnalisisQueja, id=analisisqueja_id)
    if request.method == 'POST':
        form = AnalisisQuejaForm(request.POST, instance=analisisqueja)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = AnalisisQuejaForm(instance=analisisqueja)
    return render(request, 'Gestionar Queja/editar analiss.html', {'form': form, 'analisisqueja': analisisqueja})