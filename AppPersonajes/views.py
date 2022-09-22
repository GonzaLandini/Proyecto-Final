from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import PersonajePrincipal, Compañero, Ubicacion, Avatar, UserBlog, Messenger
from .forms import AvatarForm, BlogForm, MessengerForm, PersonajePrincipalForm, UserEditForm, CompañeroForm, UbicacionForm, UserRegisterForm

def inicio(request):
    blogs=UserBlog.objects.order_by("-fechapub")[:3]
    return render(request, "App/inicio.html", {"blogs":blogs, "imagen":obtenerAvatar(request)})

def busqueda(request):
    return render(request, "App/busqueda.html", {"imagen":obtenerAvatar(request)})

def personajePrincipal(request):
    return render(request, "App/personajes.html", {"imagen":obtenerAvatar(request)})

def compañeros(request):
    return render(request, "App/compañeros.html", {"imagen":obtenerAvatar(request)})

def ubicacion(request):
    return render(request, "App/ubicaciones.html", {"imagen":obtenerAvatar(request)})

def personajeBusqueda(request):
    return render(request, "App/personajebuscar.html", {"imagen":obtenerAvatar(request)})

def personajeBuscar(request):
    if request.GET["nombre"]:
        nombrebuscado=request.GET.get("nombre")
        nombres=PersonajePrincipal.objects.filter(nombre=nombrebuscado)
        if len(nombres)!=0:
            return render(request,"App/resultadobusquedapersonaje.html", {"nombres": nombres, "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/personajebuscar.html", {"mensaje": "No existen nombres", "imagen":obtenerAvatar(request)})
    else:
        return render(request, "App/personajebuscar.html", {"mensaje": "No ingresaste ninguna busqueda!", "imagen":obtenerAvatar(request)})

def compañeroBusqueda(request):
    return render(request, "App/compañerobuscar.html", {"imagen":obtenerAvatar(request)})

def compañeroBuscar(request):
    if request.GET["nombre"]:
        nombrebuscado=request.GET.get("nombre")
        nombres=Compañero.objects.filter(nombre=nombrebuscado)
        if len(nombres)!=0:
            return render(request,"App/resultadobusquedacompañero.html", {"nombres": nombres, "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/compañerobuscar.html", {"mensaje": "No existen compañeros", "imagen":obtenerAvatar(request)})
    else:
        return render(request, "App/compañerobuscar.html", {"mensaje": "No ingresaste ninguna busqueda!", "imagen":obtenerAvatar(request)})

def ubicacionBusqueda(request):
    return render(request, "App/ubicacionbuscar.html", {"imagen":obtenerAvatar(request)})

def ubicacionBuscar(request):
    if request.GET["region"]:
        regionbuscada=request.GET.get("region")
        regiones=Ubicacion.objects.filter(region=regionbuscada)
        if len(regiones)!=0:
            return render(request,"App/resultadobusquedaubicacion.html", {"regiones": regiones, "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/ubicacionbuscar.html", {"mensaje": "No existen regiones", "imagen":obtenerAvatar(request)})
    else:
        return render(request, "App/ubicacionbuscar.html", {"mensaje": "No ingresaste ninguna busqueda!", "imagen":obtenerAvatar(request)})

def crear(request):
    return render(request, "App/crear.html", {"imagen":obtenerAvatar(request)})

def aboutMe(request):
    return render(request, "App/about.html", {"imagen":obtenerAvatar(request)})

def register(request):
    if request.method=="POST":
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                return render(request, "App/registrate.html", {"form":form, "mensaje":f"{email} ya está en uso", "imagen":obtenerAvatar(request)})
            form.save()
            return render(request, "App/inicio.html", {"mensajecorrecto":f"Usuario {username} creado!", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/registrate.html", {"form":form, "mensaje":"Uno de los campos ya existe o es inválido", "imagen":obtenerAvatar(request)})
    else:
        form=UserRegisterForm()
    return render(request, "App/registrate.html", {"form":form, "imagen":obtenerAvatar(request)})

def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usu=request.POST["username"]
            clave=request.POST["password"]
            usuario=authenticate(username=usu, password=clave)
            print(usuario)
            if usuario is not None:
                login(request, usuario)
                return render(request, "App/perfil.html", {"mensajecorrecto":f"¡Bienvenido/a {usuario}!", "imagen":obtenerAvatar(request)})
            else:
                return render(request, "App/login.html", {"form":form, "mensaje":"Usuario o contraseña incorrectos"})
        else:
            return render(request, "App/login.html", {"form":form, "mensaje":"Usuario o contraseña incorrectos"})
    else:
        form=AuthenticationForm()
        return render(request, "App/login.html", {"form":form})

@login_required
def miPerfil(request):
    return render(request, "App/perfil.html", {"imagen":obtenerAvatar(request)})

@login_required        
def editarPerfil(request):
    usuario=request.user
    miemail=request.user.email
    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            editform=form.cleaned_data
            usuario.email=editform["email"]
            if User.objects.exclude(email=miemail).filter(email=usuario.email).exists():
                return render(request, "App/editarperfil.html", {"form":form, "mensaje":f"{usuario.email} ya está en uso", "imagen":obtenerAvatar(request)})
            usuario.password1=editform["password1"]
            usuario.password2=editform["password2"]
            usuario.first_name=editform["first_name"]
            usuario.last_name=editform["last_name"] 
            usuario.save()
            print(usuario.password1)
            return render(request, 'App/perfil.html', {"mensajecorrecto": "Cambios guardados correctamente", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/editarperfil.html", {"form":form, "mensaje": "Hubo un error, revisá tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "App/editarperfil.html", {"form":form, "usuario":usuario, "imagen":obtenerAvatar(request)})

@login_required
def agregarAvatar(request):
    if request.method=="POST":
        formavatar=AvatarForm(request.POST, request.FILES)
        if formavatar.is_valid():
            avatarViejo=Avatar.objects.filter(user=request.user)
            if(len(avatarViejo)>0):
                avatarViejo.delete()
            avatar=Avatar(user=request.user, imagen=formavatar.cleaned_data["imagen"])
            avatar.save()
            return render(request, "App/agregaravatar.html", {"formavatar":formavatar, "usuario":request.user, "mensajecorrecto":"Avatar agregado", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/agregaravatar.html", {"formavatar":formavatar, "mensajealerta": "Seleccioná un archivo válido", "imagen":obtenerAvatar(request)})
    else:
        formavatar=AvatarForm()
    return render(request, "App/agregaravatar.html", {"formavatar":formavatar, "usuario":request.user, "imagen":obtenerAvatar(request)})

@login_required
def borrarAvatar(request):
    avatar=Avatar.objects.filter(user=request.user)
    avatar.delete()
    formavatar=AvatarForm()
    return render(request, "App/agregaravatar.html", {"formavatar":formavatar, "mensajecorrecto":"Avatar eliminado", "imagen":obtenerAvatar(request)})

@login_required
def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen=""
    return imagen

@login_required
def personajePrincipalForm(request):
    if request.method=="POST":
        formpersonaje=PersonajePrincipalForm(request.POST)
        if formpersonaje.is_valid():
            infopersonaje=formpersonaje.cleaned_data
            nombre=infopersonaje["nombre"]
            genero=infopersonaje["genero"]
            raza=infopersonaje["raza"]
            altura=infopersonaje["altura"]
            peso=infopersonaje["peso"]
            personaje=PersonajePrincipal(nombre=nombre, genero=genero, raza=raza, altura=altura, peso=peso)
            personaje.save()
            return render(request, "App/crear.html", {"mensajecorrecto": "Personaje creado exitosamente", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/crear.html", {"formulario": formpersonaje, "mensaje": "Hubo un error en tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        formpersonaje=PersonajePrincipalForm()
    return render(request, "App/personajeformulario.html", {"formulario": formpersonaje, "imagen":obtenerAvatar(request)})

@login_required
def compañeroForm(request):
    if request.method=="POST":
        formcompañero=CompañeroForm(request.POST)
        if formcompañero.is_valid():
            infocompañero=formcompañero.cleaned_data
            nombre=infocompañero["nombre"]
            genero=infocompañero["genero"]
            raza=infocompañero["raza"]
            compañero=Compañero(nombre=nombre, genero=genero, raza=raza)
            compañero.save()
            return render(request, "App/crear.html", {"mensajecorrecto": "Compañero creado exitosamente", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/crear.html", {"formulario": formcompañero, "mensaje": "Hubo un error en tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        formcompañero=CompañeroForm()
    return render(request, "App/compañeroformulario.html", {"formulario": formcompañero, "imagen":obtenerAvatar(request)})

@login_required
def ubicacionForm(request):
    if request.method=="POST":
        formubicacion=UbicacionForm(request.POST)
        if formubicacion.is_valid():
            infoubicacion=formubicacion.cleaned_data
            region=infoubicacion["region"]
            aldea=infoubicacion["aldea"]
            siglo=infoubicacion["siglo"]
            ubicacion=Ubicacion(region=region, aldea=aldea, siglo=siglo)
            ubicacion.save()
            return render(request, "App/crear.html", {"mensajecorrecto": "Ubicación creada exitosamente", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/crear.html", {"formulario": formubicacion, "mensaje": "Hubo un error en tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        formubicacion=UbicacionForm()
    return render(request, "App/ubicacionformulario.html", {"formulario": formubicacion, "imagen":obtenerAvatar(request)})

@login_required
def crearBlog(request):
    if request.method=="POST":
        form=BlogForm(request.POST, request.FILES)
        if form.is_valid():
            bloginfo=form.cleaned_data
            autor=request.user.username
            titulo=bloginfo["titulo"]
            subtitulo=bloginfo["subtitulo"]
            fechapub=bloginfo["fechapub"]
            imagen=bloginfo["imagen"]
            texto=bloginfo["texto"]
            blog=UserBlog(username=autor, titulo=titulo, subtitulo=subtitulo, fechapub=fechapub, imagen=imagen, texto=texto)
            blog.save()
            return render(request, "App/perfil.html", {"mensajecorrecto": "Blog creado", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/crearblog.html", {"form":form, "mensaje": "Hubo un error en tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        form=BlogForm()
    return render(request, "App/crearblog.html", {"form":form, "imagen":obtenerAvatar(request)})

def listaBlog(request):
    listablog=UserBlog.objects.all()
    return render(request, "App/listablog.html", {"listablog":listablog, "imagen":obtenerAvatar(request)})

@login_required
def leerBlog(request, id):
    blog=UserBlog.objects.get(id=id)
    return render(request, "App/blog.html", {"blog":blog, "imagen":obtenerAvatar(request)})

@login_required
def editarBlog(request, id):
    blog=UserBlog.objects.get(id=id)
    if request.method=="POST":
        form=BlogForm(request.POST, request.FILES)
        if form.is_valid():
            bloginfo=form.cleaned_data
            blog.titulo=bloginfo["titulo"]
            blog.subtitulo=bloginfo["subtitulo"]
            blog.fechapub=bloginfo["fechapub"]
            blog.imagen=bloginfo["imagen"]
            blog.texto=bloginfo["texto"]
            blog.save()
            listablog=UserBlog.objects.all()
            return render(request, "App/listablog.html", {"listablog":listablog, "mensajecorrecto": "Blog editado", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/editarblog.html", {"form":form, "mensaje": "Hubo un error en tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        form=BlogForm(initial={"titulo":blog.titulo, "subtitulo":blog.subtitulo, "fechapub":blog.fechapub, "imagen":blog.imagen, "texto":blog.texto})
        return render(request, "App/editarblog.html", {"form":form, "imagen":obtenerAvatar(request)})

@login_required
def borrarBlog(request, id):
    blog=UserBlog.objects.get(id=id)
    blog.delete()
    listablog=UserBlog.objects.all()
    return render(request, "App/listablog.html", {"listablog":listablog, "mensajecorrecto":"Blog eliminado", "imagen":obtenerAvatar(request)})

@login_required
def messenger(request):
    if request.method=="POST":
        form=MessengerForm(request.POST)
        if form.is_valid():
            mensajeform=form.cleaned_data
            emisor=request.user.username
            receptor=mensajeform["receptor"]
            mensaje=mensajeform["mensaje"]
            envio=Messenger(emisor=emisor, receptor=receptor, mensaje=mensaje)
            envio.save()
            return render(request, "App/perfil.html", {"mensajecorrecto":"Mensaje enviado", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "App/mensajes.html", {"form":form, "mensajeerror":"Hubo un error, revisá tu solicitud", "imagen":obtenerAvatar(request)})
    else:
        form=MessengerForm()
        return render(request, "App/mensajes.html", {"form":form, "imagen":obtenerAvatar(request)})

@login_required
def mensajeBuscar(request):
    receptor=request.user
    mensajes=Messenger.objects.filter(receptor=receptor)
    if len(mensajes)>0:
        return render(request,"App/mismensajes.html", {"mensajes": mensajes, "imagen":obtenerAvatar(request)})
    else:
        return render(request, "App/perfil.html", {"mensajealerta":"No tenés mensajes", "imagen":obtenerAvatar(request)})

@login_required
def borrarMensaje(request, id):
    receptor=request.user
    mensaje=Messenger.objects.get(id=id)
    mensaje.delete()
    mensajes=Messenger.objects.filter(receptor=receptor)
    if len(mensajes)>0:
        return render(request,"App/mismensajes.html", {"mensajes": mensajes, "mensajecorrecto":"Mensaje borrado", "imagen":obtenerAvatar(request)})
    else:
        return render(request, "App/perfil.html", {"mensajealerta":"No tenés mensajes", "imagen":obtenerAvatar(request)})