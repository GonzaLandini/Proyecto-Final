from datetime import datetime
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PersonajePrincipal(models.Model):
    nombre=models.CharField(max_length=50)
    genero=models.CharField(max_length=50)
    raza=models.CharField(max_length=50)
    altura=models.IntegerField()
    peso=models.IntegerField()

    def __str__(self) -> str:
        return self.nombre+", "+self.raza

class Compañero(models.Model):
    nombre=models.CharField(max_length=50)
    genero=models.CharField(max_length=50)
    raza=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nombre+", "+self.raza

class Ubicacion(models.Model):
    region=models.CharField(max_length=50)
    aldea=models.CharField(max_length=50)
    siglo=models.IntegerField() 

    def __str__(self) -> str:
        return self.region

class Avatar(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    imagen= models.ImageField(upload_to='avatares', null=True, blank=True)

class UserBlog(models.Model):
    username=models.CharField(max_length=50)
    titulo=models.CharField(max_length=50)
    subtitulo=models.CharField(max_length=100)
    fechapub=models.DateField(default=datetime.now)
    imagen=models.ImageField(upload_to='blogs', null=True, blank=True)
    texto=RichTextField(max_length=2000)

    def __str__(self) -> str:
        return str(self.username)+", "+self.titulo
        
class Messenger(models.Model):
    emisor=models.CharField(max_length=50, null=True)
    receptor=models.CharField(max_length=50, null=True)
    mensaje=models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return "De: "+str(self.emisor)+", Para: "+str(self.receptor)