from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.cache import never_cache
from .forms import CustomUserCreationForm




@never_cache
def logear(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dash')
        else:
            error_message = 'Credenciales Invalidas'
    else:
        error_message = None


    return render(request, 'Autenticacion/login2.html', {'error_message': error_message})

@login_required
@never_cache
def cerrar_sesion(request):
    logout(request)
    return redirect('autenticacion')

@never_cache
class VRegistro(View):
    def get (self,request):
        form=UserCreationForm()
        return render(request,"Autenticacion/login2.html",{"form":form})

@never_cache
def post (self,request):
   pass


@never_cache
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('listar_quejasU')
        else:
            error_message = 'El formulario contiene los siguientes errores:<br>'
            for field, errors in form.errors.items():
                error_message += f'- {field}: {", ".join(errors)}<br>'
    else:
        form = CustomUserCreationForm()
    return render(request, 'Autenticacion/login2.html', {'form': form,'error_message':error_message})
