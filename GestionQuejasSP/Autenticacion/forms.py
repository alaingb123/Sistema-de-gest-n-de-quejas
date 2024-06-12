

from django.contrib.auth.models import User,Group,Permission
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm





class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')