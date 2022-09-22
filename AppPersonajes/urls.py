from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path("", inicio, name="inicio"),
    path("about/", aboutMe, name="aboutme"),
    path("login/", login_request, name="login"),
    path("logout/", LogoutView.as_view(template_name="App/logout.html"), name="logout"),
    path("registrate/", register, name="registrate"),
    path("perfil/", miPerfil, name="perfil"),
    path("perfil/editarperfil/", editarPerfil, name="editarperfil"),
    path("perfil/agregaravatar/", agregarAvatar, name="agregaravatar"),
    path("perfil/agregaravatar/eliminar/", borrarAvatar, name="borraravatar"),
    path("crearblog/", crearBlog, name="crearblog"),
    path("editarblog/<int:id>", editarBlog, name="editarblog"),
    path("listablog/", listaBlog, name="listablog"),
    path("listablog/<int:id>/", leerBlog, name="blog"),
    path("listablog/borrarblog/<int:id>/", borrarBlog, name="borrarblog"),
    path("mensajes/", messenger, name="mensajes"),
    path("mismensajes/", mensajeBuscar, name="mismensajes"),
    path("mismensajes/borrarmensaje/<int:id>", borrarMensaje, name="borrarmensaje"),

    path("personajes/", personajePrincipal, name="personajes"),
    path("busqueda/personaje/", personajeBusqueda, name="personajebuscar"),
    path("personajeformulario/", personajePrincipalForm, name="personajeformulario"),
    path("resultadobusquedapersonaje/", personajeBuscar, name="resultadobusquedapersonaje" ),
    
    path("compañeros/", compañeros, name="compañeros"),
    path("busqueda/compañero/", compañeroBusqueda, name="compañerobuscar"),
    path("compañeroformulario/", compañeroForm, name="compañeroformulario"),
    path("resultadobusquedacompañero/", compañeroBuscar, name="resultadobusquedacompañero"),

    path("ubicaciones/", ubicacion, name="ubicaciones"),
    path("ubicacionbuscar/", ubicacionBusqueda, name="ubicacionbuscar"),
    path("ubicacionformulario/", ubicacionForm, name="ubicacionformulario"),    
    path("resultadobusquedaubicacion/", ubicacionBuscar, name="resultadobusquedaubicacion"),
        
    path("crear/", crear, name="crear"),
    path("busqueda/", busqueda, name="busqueda"),
]