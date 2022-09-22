from ckeditor.widgets import CKEditorWidget
from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Crear clases acá

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(label="e-mail", max_length=50)
    password1=forms.CharField(label="Contraseña", min_length=5, max_length=20, widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar contraseña", min_length=5, max_length=20, widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=["username", "email", "password1", "password2"]
        help_texts={k:"" for k in fields}

class UserEditForm(UserCreationForm):
    email=forms.EmailField(label="Modificar e-mail")
    password1=forms.CharField(label="Modificar contraseña", min_length=5, widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar contraseña", min_length=5, widget=forms.PasswordInput)
    first_name=forms.CharField(label="Modificar Nombre", required=None)
    last_name=forms.CharField(label="Modificar Apellido", required=None)
    
    class Meta:
        model=User
        fields=["email", "password1", "password2", "first_name", "last_name"]
        help_texts={k:"" for k in fields}

class AvatarForm(forms.Form):
    imagen=forms.ImageField(label="Imagen")

class PersonajePrincipalForm(forms.Form):
    nombre=forms.CharField(max_length=50)
    genero=forms.CharField(max_length=50)
    raza=forms.CharField(max_length=50)
    altura=forms.IntegerField()
    peso=forms.IntegerField()

class CompañeroForm(forms.Form):
    nombre=forms.CharField(max_length=50)
    genero=forms.CharField(max_length=50)
    raza=forms.CharField(max_length=50)

class UbicacionForm(forms.Form):
    region=forms.CharField(max_length=50)
    aldea=forms.CharField(max_length=50)
    siglo=forms.IntegerField()

class BlogForm(forms.Form):
    titulo=forms.CharField(max_length=50, label="Titulo Blog * ")
    subtitulo=forms.CharField(max_length=100, label="Subtitulo * ")
    fechapub=forms.DateField(widget=forms.SelectDateWidget, label="Fecha de publicacion * ", initial=date.today)
    imagen=forms.ImageField(label="Adjuntar imagen (opcional)", required=None)
    texto=forms.CharField(max_length=2000, label="Contenido Blog * (max. 2000 caracteres)", widget=CKEditorWidget())

class MessengerForm(forms.Form):           
    usuarios=User.objects.values_list("username","username")
    receptor=forms.ChoiceField(label="Para", widget=forms.Select, choices=usuarios)
    mensaje=forms.CharField(max_length=500, label="Mensaje", widget=forms.Textarea)