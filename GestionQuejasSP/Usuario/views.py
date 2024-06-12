from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
# from .models import User
from django.contrib.auth.models import User,Group,Permission
from .forms import UserForm, GroupForm, CustomUserCreationForm, UserEditForm, CrearUsuarioFormulario
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from django.views.generic.edit import ContextMixin

from django.contrib.auth.views import PasswordChangeView

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'Gestionar Usuario/change_password.html'
    form_class = PasswordChangeForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['old_password'].widget.attrs['style'] = 'background-color: rgba(255,255,255,0)'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['style'] = 'background-color: rgba(255,255,255,0)'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['style'] = 'background-color: rgba(255,255,255,0)'
        return form

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def user_list(request):
    users = User.objects.all()
    # Crear un objeto Paginator con las quejas y la cantidad de elementos por página
    paginator = Paginator(users, 10)

    # Obtener el número de página actual
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Gestionar Usuario/user_list.html', {'page_obj': page_obj})

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def create_user(request):

    error_message=''
    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            groups = form.cleaned_data.get('groups')
            for group in groups:
                group.user_set.add(user)
            return redirect('user_list')
        else:

            # Si los datos no son válidos, recopilar los mensajes de error del formulario
            error_message = 'El formulario contiene los siguientes errores:<br>'
            for field, errors in form.errors.items():
                error_message += f'- {field}: {", ".join(errors)}<br>'
    else:
        form = CustomUserCreationForm()
    return render(request, 'Gestionar Usuario/user_prueba_create.html', {'form': form, 'error_message': error_message})

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def edit_user(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'Gestionar Usuario/user_form2.html', {'form': form,'user':user})




@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if(user):
        user.delete()
        return redirect('user_list')


@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            permissions = form.cleaned_data['permissions']
            group.save()
            group.permissions.set(permissions)
            return redirect('grupoL')
    else:
        form = GroupForm()
    return render(request, 'Gestionar Usuario/crearGrupo.html', {'form': form})

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def group_edit(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            permissions = form.cleaned_data['permissions']
            group.save()
            group.permissions.set(permissions)
            return redirect('grupoL')
    else:
        form = GroupForm(instance=group)
    return render(request, 'Gestionar Usuario/editarGrupo.html', {'form': form, 'group': group})

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'Gestionar Usuario/group_list.html', {'groups': groups})

@never_cache
@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def delete_group(request, pk):

    group = get_object_or_404(Group, pk=pk)


    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Grupo eliminado exitosamente.')
        return redirect('grupoL')
    else:
        messages.error(request, 'Error al eliminar el grupo.')
    return redirect('grupoL')


@login_required()
def password_change_done (request):
    return render(request,'Gestionar Usuario/password_change_done.html')



from django.shortcuts import render, get_object_or_404, redirect
from GestionQuejasAPP.models import Clasificacion,Conclusion,Satisfaccion,CasoPrensa,Procedencia,Via,Modalidad,EntidadAfectada
from .forms import ClasificacionForm,ViaForm,ModalidadForm,SatisfaccionForm,ProcedenciaForm,ConclusionForm,CasoPrensaForm,EntidadAfectadaForm


from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

def es_moderador(user):
    return user.groups.filter(name='Moderador').exists()

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_moderador), name='dispatch')
class ClasificacionListView(ListView):
    model = Clasificacion
    template_name = 'Gestionar Usuario/Lista desplegable/list.html'
    context_object_name = 'clasificaciones'
    queryset = Clasificacion.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entidades'] = EntidadAfectada.objects.all()
        context['concluciones'] = Conclusion.objects.all()
        context['satisfacciones'] = Satisfaccion.objects.all()
        context['casos'] = CasoPrensa.objects.all()
        context['procedencias'] = Procedencia.objects.all()
        context['vias'] = Via.objects.all()
        context['modalidades'] = Modalidad.objects.all()
        return context



 # Clasificacion crud--------------------------------------------------------------------
from django.views.generic.edit import CreateView

@method_decorator(user_passes_test(es_moderador), name='dispatch')
class ClasificacionCreateView(CreateView):
    model = Clasificacion
    form_class = ClasificacionForm
    template_name = 'Gestionar Usuario/Lista desplegable/create.html'
    success_url = reverse_lazy('list_desp')  # Redirige a la lista después de crear

    # Opcional: puedes personalizar el contexto si es necesario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega más datos al contexto si es necesario
        return context

from django.views.generic.edit import UpdateView

@method_decorator(user_passes_test(es_moderador), name='dispatch')
class ClasificacionUpdateView(UpdateView):
    model = Clasificacion
    form_class = ClasificacionForm
    template_name = 'Gestionar Usuario/Lista desplegable/edit.html'
    success_url = reverse_lazy('list_desp')  # Redirige a la lista después de editar

    # Opcional: puedes personalizar el contexto si es necesario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega más datos al contexto si es necesario
        return context

@method_decorator(user_passes_test(es_moderador), name='dispatch')
class ClasificacionDeleteView(DeleteView):
    model = Clasificacion
    template_name = 'Gestionar Usuario/Lista desplegable/delete.html'
    success_url = reverse_lazy('list_desp')  # Redirige a la lista después de eliminar

    # Opcional: puedes personalizar el contexto si es necesario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega más datos al contexto si es necesario
        return context




 # Conclusion crud-------------------------------------------------------------------------------

@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def conclusion_new(request):
    if request.method == "POST":
        form = ConclusionForm(request.POST)
        if form.is_valid():
            conclusion = form.save(commit=False)
            conclusion.save()
            return redirect('list_desp')
    else:
        form = ConclusionForm()
    return render(request, 'Gestionar Usuario/Lista desplegable/create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def conclusion_edit(request, pk):
    conclusion = get_object_or_404(Conclusion, pk=pk)
    if request.method == "POST":
        form = ConclusionForm(request.POST, instance=conclusion)
        if form.is_valid():
            conclusion = form.save(commit=False)
            conclusion.save()
            return redirect('list_desp')
    else:
        form = ConclusionForm(instance=conclusion)
    return render(request, 'Gestionar Usuario/Lista desplegable/edit.html', {'form': form,'clasificacion':conclusion})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def conclusion_delete(request, pk):
    conclusion = get_object_or_404(Conclusion, pk=pk)
    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        conclusion.delete()
        return redirect('list_desp')
    else:
        return render(request, 'Gestionar Usuario/Lista desplegable/delete.html',
                  {'clasificacion': conclusion})



# entidades crud------------------------------------------------------------------------------------


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def enti_new(request):
    if request.method == "POST":
        form = EntidadAfectadaForm(request.POST)
        if form.is_valid():
            enti = form.save(commit=False)
            enti.save()
            return redirect('list_desp')
    else:
        form = EntidadAfectadaForm()
    return render(request, 'Gestionar Usuario/Lista desplegable/create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def enti_edit(request, pk):
    enti = get_object_or_404(EntidadAfectada, pk=pk)
    if request.method == "POST":
        form = EntidadAfectadaForm(request.POST, instance=enti)
        if form.is_valid():
            enti = form.save(commit=False)
            enti.save()
            return redirect('list_desp')
    else:
        form = EntidadAfectadaForm(instance=enti)
    return render(request, 'Gestionar Usuario/Lista desplegable/edit.html', {'form': form,'clasificacion':enti})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def enti_delete(request, pk):
    enti = get_object_or_404(EntidadAfectada, pk=pk)
    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        enti.delete()
        return redirect('list_desp')
    else:
        return render(request, 'Gestionar Usuario/Lista desplegable/delete.html',
                  {'clasificacion': enti})


# satisfacciones crud------------------------------------------------------------------------------------

@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def satis_new(request):
    if request.method == "POST":
        form = SatisfaccionForm(request.POST)
        if form.is_valid():
            satis = form.save(commit=False)
            satis.save()
            return redirect('list_desp')
    else:
        form = SatisfaccionForm()
    return render(request, 'Gestionar Usuario/Lista desplegable/create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def satis_edit(request, pk):
    satis = get_object_or_404(Satisfaccion, pk=pk)
    if request.method == "POST":
        form = SatisfaccionForm(request.POST, instance=satis)
        if form.is_valid():
            satis = form.save(commit=False)
            satis.save()
            return redirect('list_desp')
    else:
        form = SatisfaccionForm(instance=satis)
    return render(request, 'Gestionar Usuario/Lista desplegable/edit.html', {'form': form,'clasificacion':satis})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def satis_delete(request, pk):
    satis = get_object_or_404(Satisfaccion, pk=pk)
    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        satis.delete()
        return redirect('list_desp')
    else:
        return render(request, 'Gestionar Usuario/Lista desplegable/delete.html',
                  {'clasificacion': satis})



# caso crud------------------------------------------------------------------------------------


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def caso_new(request):
    if request.method == "POST":
        form = CasoPrensaForm(request.POST)
        if form.is_valid():
            caso = form.save(commit=False)
            caso.save()
            return redirect('list_desp')
    else:
        form = CasoPrensaForm()
    return render(request, 'Gestionar Usuario/Lista desplegable/create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def caso_edit(request, pk):
    caso = get_object_or_404(CasoPrensa, pk=pk)
    if request.method == "POST":
        form = CasoPrensaForm(request.POST, instance=caso)
        if form.is_valid():
            caso = form.save(commit=False)
            caso.save()
            return redirect('list_desp')
    else:
        form = CasoPrensaForm(instance=caso)
    return render(request, 'Gestionar Usuario/Lista desplegable/edit.html', {'form': form,'clasificacion':caso})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def caso_delete(request, pk):
    caso = get_object_or_404(CasoPrensa, pk=pk)
    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        caso.delete()
        return redirect('list_desp')
    else:
        return render(request, 'Gestionar Usuario/Lista desplegable/delete.html',
                  {'clasificacion': caso})


# moda crud------------------------------------------------------------------------------------


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def moda_new(request):
    if request.method == "POST":
        form = ModalidadForm(request.POST)
        if form.is_valid():
            moda = form.save(commit=False)
            moda.save()
            return redirect('list_desp')
    else:
        form = ModalidadForm()
    return render(request, 'Gestionar Usuario/Lista desplegable/create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def moda_edit(request, pk):
    moda = get_object_or_404(Modalidad, pk=pk)
    if request.method == "POST":
        form = ModalidadForm(request.POST, instance=moda)
        if form.is_valid():
            moda = form.save(commit=False)
            moda.save()
            return redirect('list_desp')
    else:
        form = ModalidadForm(instance=moda)
    return render(request, 'Gestionar Usuario/Lista desplegable/edit.html', {'form': form,'clasificacion':moda})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def moda_delete(request, pk):
    moda = get_object_or_404(Modalidad, pk=pk)
    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        moda.delete()
        return redirect('list_desp')
    else:
        return render(request, 'Gestionar Usuario/Lista desplegable/delete.html',
                  {'clasificacion': moda})


# via crud------------------------------------------------------------------------------------


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def via_new(request):
    if request.method == "POST":
        form = ViaForm(request.POST)
        if form.is_valid():
            via = form.save(commit=False)
            via.save()
            return redirect('list_desp')
    else:
        form = ViaForm()
    return render(request, 'Gestionar Usuario/Lista desplegable/create.html', {'form': form})

@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def via_edit(request, pk):
    via = get_object_or_404(Via, pk=pk)
    if request.method == "POST":
        form = ViaForm(request.POST, instance=via)
        if form.is_valid():
            via = form.save(commit=False)
            via.save()
            return redirect('list_desp')
    else:
        form = ViaForm(instance=via)
    return render(request, 'Gestionar Usuario/Lista desplegable/edit.html', {'form': form,'clasificacion':via})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def via_delete(request, pk):
    via = get_object_or_404(Via, pk=pk)
    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        via.delete()
        return redirect('list_desp')
    else:
        return render(request, 'Gestionar Usuario/Lista desplegable/delete.html',
                  {'clasificacion': via})


# procedencia crud------------------------------------------------------------------------------------


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def procedencia_new(request):
    if request.method == "POST":
        form = ProcedenciaForm(request.POST)
        if form.is_valid():
            procedencia = form.save(commit=False)
            procedencia.save()
            return redirect('list_desp')
    else:
        form = ProcedenciaForm()
    return render(request, 'Gestionar Usuario/Lista desplegable/create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def procedencia_edit(request, pk):
    procedencia = get_object_or_404(Procedencia, pk=pk)
    if request.method == "POST":
        form = ProcedenciaForm(request.POST, instance=procedencia)
        if form.is_valid():
            procedencia = form.save(commit=False)
            procedencia.save()
            return redirect('list_desp')
    else:
        form = ProcedenciaForm(instance=procedencia)
    return render(request, 'Gestionar Usuario/Lista desplegable/edit.html', {'form': form,'clasificacion':procedencia})


@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def procedencia_delete(request, pk):
    procedencia = get_object_or_404(Procedencia, pk=pk)
    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        procedencia.delete()
        return redirect('list_desp')
    else:
        return render(request, 'Gestionar Usuario/Lista desplegable/delete.html',
                  {'clasificacion': procedencia})



@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def confirmiar_eliminacion(request, pk):
        user = get_object_or_404(User, pk=pk)

        if request.method == 'POST':
            # Hacer algo cuando se presiona el botón "Eliminar"
            user.delete()
            return redirect('user_list')
        else:
            return render(request, 'Gestionar Usuario/confirmar_eliminacion_de_usuario.html',
                          {'user': user})



@user_passes_test(lambda u: u.groups.filter(name='Moderador').exists())
def confirmiar_eliminacion_group(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        # Hacer algo cuando se presiona el botón "Eliminar"
        group.delete()
        return redirect('grupoL')
    else:
        return render(request, 'Gestionar Usuario/confirmar_eliminacion_de_grupo.html',
                      {'group': group})


def crear_usuario(request):
    messages_s=None
    messages=None
    if request.method == 'POST':
        formulario = CrearUsuarioFormulario(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages_s="Registro exitoso"
        else:
            messages = formulario.errors
    else:
        formulario = CrearUsuarioFormulario()

    return render(request, 'Autenticacion/login2.html', {'formulario': formulario, 'error_message': messages,"messages_s":messages_s})

# import random
# import string
# from datetime import datetime, timedelta
# from GestionQuejasAPP.models import EntidadAfectada, Modalidad, Via, Procedencia, Clasificacion, CasoPrensa, Queja
# from django.contrib.auth.models import User
#
#
# def generate_argument():
#     # Lista de párrafos predefinidos que se pueden combinar
#     paragraphs = [
#         "Desde hace varias semanas vengo presentando problemas con el servicio de esta entidad. En reiteradas ocasiones he intentado comunicarme con el centro de atención al cliente, sin obtener una solución satisfactoria a mi solicitud.",
#         "El día [FECHA], acudí personalmente a las instalaciones de la entidad y fui atendido de manera inadecuada por uno de sus funcionarios. No se me brindó la información necesaria ni se tomaron las acciones pertinentes para resolver mi caso.",
#         "Como consecuencia de la negligencia y falta de diligencia por parte de esta entidad, me he visto perjudicado económicamente. Los inconvenientes presentados me han generado gastos adicionales que espero sean resarcidos.",
#         "Solicito de manera urgente que se revise mi caso y se tomen las medidas necesarias para subsanar los perjuicios ocasionados. Espero contar con una respuesta oportuna y una solución efectiva a la mayor brevedad posible.",
#         "Es lamentable que, a pesar de ser un cliente con varios años de antigüedad, no haya recibido un trato adecuado por parte de esta entidad. Confío en que se pueda llegar a una solución que satisfaga mis legítimas reclamaciones."
#     ]
#
#     # Seleccionar 3-5 párrafos aleatoriamente y combinarlos en un argumento
#     num_paragraphs = random.randint(3, 5)
#     argument = "\n\n".join([random.choice(paragraphs) for _ in range(num_paragraphs)])
#
#     # Reemplazar [FECHA] con una fecha aleatoria
#     fecha = datetime.now() - timedelta(days=random.randint(1, 90))
#     argument = argument.replace("[FECHA]", fecha.strftime("%d de %B de %Y"))
#
#     return argument
# def generate_name():
#     first_names = ['Alejandro', 'Ángela', 'Carlos', 'Daniela', 'Ernesto', 'Fernanda', 'Gilberto', 'Isabela', 'José', 'Mariana', 'Óscar', 'Paola', 'Raúl', 'Sofía', 'Tomás', 'Valentina', 'William', 'Ximena', 'Yolanda', 'Zambrano']
#     last_names = ['Acosta', 'Díaz', 'Fernández', 'García', 'González', 'Hernández', 'Jiménez', 'López', 'Martínez', 'Morales', 'Núñez', 'Peña', 'Reyes', 'Rodríguez', 'Sánchez', 'Torres', 'Valdés', 'Vargas', 'Vega', 'Zamora']
#     return f"{random.choice(first_names)} {random.choice(last_names)}"
#
# def generate_address():
#     street_names = ['Calle Principal', 'Avenida de los Álamos', 'Paseo de la Reforma', 'Carrera 7', 'Calle del Sol', 'Avenida Suba', 'Calle Real', 'Carrera 10', 'Calle Ancha', 'Avenida Bolívar']
#     street_types = ['Calle', 'Avenida', 'Carrera', 'Pasaje', 'Callejón', 'Camino']
#     city_names = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Bucaramanga', 'Cúcuta', 'Pereira', 'Santa Marta', 'Manizales']
#     states = ['Antioquia', 'Cundinamarca', 'Valle del Cauca', 'Atlántico', 'Bolívar', 'Santander', 'Norte de Santander', 'Risaralda', 'Magdalena', 'Caldas']
#     street_number = random.randint(1, 999)
#     street_name = f"{random.choice(street_types)} {random.choice(street_names)}"
#     city = random.choice(city_names)
#     state = random.choice(states)
#     return f"{street_number} {street_name}, {city}, {state}"
#
# def generate_subject():
#     subject_prefixes = ['Reclamo por', 'Queja sobre', 'Solicitud de', 'Inconformidad con', 'Denuncia de', 'Reporte de']
#     subject_topics = ['servicio deficiente', 'incumplimiento de políticas', 'daños en propiedad', 'trato inadecuado', 'demora en respuesta', 'problemas con facturación']
#     return f"{random.choice(subject_prefixes)} {random.choice(subject_topics)}"
#
# # Crea 800 quejas
# for i in range(800):
#     queja = Queja(
#         nombre_apellidos=generate_name(),
#         entidadAfectada=random.choice(EntidadAfectada.objects.all()),
#         modalidad=random.choice(Modalidad.objects.all()),
#         via=random.choice(Via.objects.all()),
#         procedencia=random.choice(Procedencia.objects.all()),
#         clasificacion=random.choice(Clasificacion.objects.all()),
#         casoPrensa=random.choice(CasoPrensa.objects.all()),
#         fechaR=datetime.now() - timedelta(days=random.randint(1, 365)),
#         fechaT=datetime.now() - timedelta(days=random.randint(1, 365)),
#         asunto=generate_subject(),
#         argumento=generate_argument(),
#         telefono=random.randint(10000000, 99999999),
#         direccion=generate_address(),
#         usuario_created=random.choice(User.objects.all()),
#         usuario_update=random.choice(User.objects.all()),
#     )
#     queja.save()
#     print(i)