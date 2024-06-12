from django import forms
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class UserForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Email is required.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])
        return user


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    is_active = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'is_active', 'password1', 'password2')





class GroupForm(forms.ModelForm):
    name = forms.CharField(max_length=15)
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class UserEditForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'groups']







from GestionQuejasAPP.models import Clasificacion,EntidadAfectada,Modalidad,Via,Procedencia,CasoPrensa,Satisfaccion,Conclusion

class ClasificacionForm(forms.ModelForm):

    class Meta:
        model = Clasificacion
        fields = ('nombre',)


class EntidadAfectadaForm(forms.ModelForm):
    class Meta:
        model = EntidadAfectada
        fields = ('nombre',)

class ModalidadForm(forms.ModelForm):
    class Meta:
        model = Modalidad
        fields = ('nombre',)

class ViaForm(forms.ModelForm):
    class Meta:
        model = Via
        fields = ('nombre',)

class ProcedenciaForm(forms.ModelForm):
    class Meta:
        model = Procedencia
        fields = ('nombre',)

class CasoPrensaForm(forms.ModelForm):
    class Meta:
        model = CasoPrensa
        fields = ('nombre',)

class SatisfaccionForm(forms.ModelForm):
    class Meta:
        model = Satisfaccion
        fields = ('nombre',)

class ConclusionForm(forms.ModelForm):
    class Meta:
        model = Conclusion
        fields = ('nombre',)




class CrearUsuarioFormulario(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')




