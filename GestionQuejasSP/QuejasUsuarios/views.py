# Create your views here.

from django.shortcuts import render, redirect,get_object_or_404
from .forms import QuejaUForm,FiltroQuejasForm
from datetime import datetime
from .models import QuejaU, DocumentoQU
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from GestionQuejasAPP.forms import QuejaForm, RespuestaForm, ModificarRespuestaForm,FormMeses
from GestionQuejasAPP.models import Satisfaccion,Respuesta,Queja
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.http import Http404



yearu=datetime.now().year;



@method_decorator(login_required, name='dispatch')
class InsertarQuejaView(CreateView):
    model = QuejaU
    form_class = QuejaUForm
    template_name = 'QuejasU/insertar_quejaU.html'
    success_url = reverse_lazy('listar_quejasU')

    def form_valid(self, form):
        queja = form.save(commit=False)
        queja.usuario = self.request.user
        queja.save()
        documentos = self.request.FILES.getlist('documento')
        for archivo in documentos:
            DocumentoQU.objects.create(quejaU=queja, archivo=archivo)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


from django.db.models import Case, When, Value, IntegerField

@login_required
def listar_queja(request):
    now = datetime.now()
    now = now.date()
    # Obtener el año actual
    current_year = datetime.now().year

    # Obtener el valor del campo years del formulario
    year = request.GET.get('years', current_year)

    global yearu
    yearu = year

    quejas = QuejaU.objects.filter(created__year=year)

    form = FiltroQuejasForm(initial={'years': year})


    numero = request.GET.get('numero')
    nombre = request.GET.get('nombre_apellidos')

    grupos = request.user.groups.all()

    is_f=False
    for grupo in grupos:
        if grupo.name=="Funcionario":
            is_f=True

    if is_f is False:
        quejas=quejas.filter(usuario=request.user)


    if numero:
        quejas = quejas.filter(queja_us__numero=numero)


    if nombre:
        quejas=quejas.filter(nombre_apellidos__icontains=nombre)


    if request.method == 'GET':
        meses = FormMeses(request.GET)
        if meses.is_valid():
            mes = meses.cleaned_data['mes']
            dia = meses.cleaned_data['dias']
            # Aquí puedes procesar los datos enviados por el usuario
            if mes:
                quejas = quejas.filter(created__month=mes)
            if dia:
                quejas = quejas.filter(created__day=dia)
    else:
        meses = FormMeses()


    if 'registrada' in request.GET:
        quejas = quejas.filter(queja_us__numero__isnull=False)
        quejas=quejas.order_by('queja_us__numero')
    else:
        if is_f is True:
            quejas=quejas.filter(queja_us__numero__isnull=True)

    quejas = quejas.annotate(
        tiene_numero=Case(
            When(queja_us__numero__isnull=False, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-tiene_numero', 'queja_us__numero')

    # Crear un objeto Paginator con las quejas y la cantidad de elementos por página
    paginator = Paginator(quejas, 4)  # 10 elementos por página

    # Obtener el número de página actual
    page_number = request.GET.get('page')
    page = "page=" + str(page_number)

    # Obtener la página correspondiente al número de página actual
    page_obj = paginator.get_page(page_number)

    search_params = request.GET.copy()
    search_params = search_params.urlencode()

    if page in search_params:
        search_params = search_params.replace(page, "")

    registrada = request.GET.get('registrada')

    cantidad = quejas.count()

    anos = Queja.objects.dates('fechaR', 'year').distinct()

    # Obtener el valor del campo years del formulario
    year = request.GET.get('years', current_year)

    years = [anno.year for anno in anos]
    anos=years

    return render(request,'QuejasU/lista_quejasU.html', {'quejas': page_obj,
                                                         'search_params':search_params,
                                                         'page_obj':page_obj,
                                                         'meses':meses,
                                                         'form':form,
                                                         'cantidad':cantidad,
                                                         'registrada':registrada,
                                                         'mes':mes,
                                                         'dia':dia,
                                                         'anos':anos,
                                                         'year':year,
                                                         'now':now
                                                         })





@method_decorator(login_required, name='dispatch')
class EditarQuejaView(LoginRequiredMixin, UpdateView):
    model = QuejaU
    form_class = QuejaUForm
    template_name = 'QuejasU/editar_queja.html'
    success_url = reverse_lazy('listar_quejasU')

    def get_initial(self):
        initial = super().get_initial()
        queja = self.get_object()
        initial['nombre_apellidos'] = queja.nombre_apellidos
        initial['asunto'] = queja.asunto
        initial['telefono'] = queja.telefono
        initial['direccion'] = queja.direccion
        initial['argumento'] = queja.argumento
        return initial

    def dispatch(self, request, *args, **kwargs):
        queja = self.get_object()
        if request.user != queja.usuario:
            messages.error(request, 'No tienes permiso para editar esta queja.')
            return redirect('listar_quejasU')
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'El formulario es inválido. Por favor, corrige los errores.')
        return super().form_invalid(form)

    def form_valid(self, form):
        queja_vieja = self.get_object()
        for docu in queja_vieja.documentos.all():
            docu.delete()
        messages.success(self.request, 'La queja se ha actualizado correctamente.')
        response = super().form_valid(form)
        quejau = form.save(commit=False)
        form.save()  # Guardar los cambios en la base de datos

        documentos = self.request.FILES.getlist('documento')
        for archivo in documentos:
            DocumentoQU.objects.create(quejaU=quejau, archivo=archivo)
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        queja = self.get_object()
        kwargs['instance'] = queja
        return kwargs


@login_required
def eliminar_queja(request, numero):
    queja = get_object_or_404(QuejaU, id=numero)

    # Verificar si el usuario actual es el creador de la queja
    if request.user != queja.usuario:
        messages.error(request, 'No tienes permiso para eliminar esta queja.')
        return redirect('listar_quejasU')


    if request.method == 'POST':
        queja.delete()
        messages.success(request, 'La queja se ha eliminado correctamente.')
        return redirect('listar_quejasU')
    return redirect('listar_quejasU')

from django.urls import reverse
from django.http import HttpResponseRedirect
# @login_required
# def ver_queja(request, numero):
#
#     queja=get_object_or_404(QuejaU,id=numero)
#
#
#
#
#     satisfaccion = Satisfaccion.objects.all()
#     fecha_actual = datetime.today().strftime('%Y-%m-%d')
#
#     if request.method == 'POST':
#         # Obtener los valores del formulario POST
#         satis = request.POST.get('satisfaccion')
#         fechaE = request.POST.get('fechaE')
#
#         satisfaccion1 = Satisfaccion.objects.get(id=satis)
#
#         # Actualizar el objeto Respuesta y guardarlo en la base de datos
#         respuesta = queja.queja_us.respuesta
#         respuesta.__class__.objects.filter(id=respuesta.id).update(satisfaccion=satisfaccion1, entrega=True,
#                                                                   fechaE=fechaE)
#
#
#
#         # respuesta.satisfaccion = satisfaccion1
#         # respuesta.entrega = True
#         # respuesta.fechaE = fechaE
#         # respuesta.save()
#
#         # Redirigir a la página de detalles de la queja
#         return HttpResponseRedirect(reverse('ver_detalles', args=[numero]))
#
#     return render(request, 'QuejasU/ver_detalles.html',
#                   {'queja': queja, 'satisfaccion': satisfaccion, 'fecha_actual': fecha_actual})

from django.http import HttpResponseNotFound

def ver_queja(request, numero):
    try:
        queja = get_object_or_404(QuejaU, id=numero)
        satisfaccion = Satisfaccion.objects.all()
        fecha_actual = datetime.today().strftime('%Y-%m-%d')

        if request.method == 'POST':
            satis = request.POST.get('satisfaccion')
            fechaE = request.POST.get('fechaE')

            satisfaccion1 = Satisfaccion.objects.get(id=satis)

            # Actualizar el objeto Respuesta y guardarlo en la base de datos
            respuesta = queja.queja_us.respuesta
            respuesta.__class__.objects.filter(id=respuesta.id).update(satisfaccion=satisfaccion1, entrega=True,
                                                                       fechaE=fechaE)

        return render(request, 'QuejasU/ver_detalles.html', {'queja': queja, 'satisfaccion': satisfaccion, 'fecha_actual': fecha_actual})
    except Http404:
        return HttpResponseNotFound('La queja no existe')
@login_required
def ver_queja2(request, id):
    try:
        queja=get_object_or_404(Queja,id=id)

        queja=queja.queja_u
        numero=queja.id



        satisfaccion = Satisfaccion.objects.all()
        fecha_actual = datetime.today().strftime('%Y-%m-%d')

        if request.method == 'POST':
            # Obtener los valores del formulario POST
            satis = request.POST.get('satisfaccion')
            fechaE = request.POST.get('fechaE')

            satisfaccion1 = Satisfaccion.objects.get(id=satis)

            # Actualizar el objeto Respuesta y guardarlo en la base de datos
            respuesta = queja.queja_us.respuesta
            respuesta.satisfaccion = satisfaccion1
            respuesta.entrega = True
            respuesta.fechaE = fechaE
            respuesta.save()

            # Redirigir a la página de detalles de la queja
            return HttpResponseRedirect(reverse('ver_detalles', args=[numero]))

        return render(request, 'QuejasU/ver_detalles.html',
                      {'queja': queja, 'satisfaccion': satisfaccion, 'fecha_actual': fecha_actual})
    except Http404:
        messages.error(request, 'La queja ya no existe')
        return redirect('ver_notificacion')



