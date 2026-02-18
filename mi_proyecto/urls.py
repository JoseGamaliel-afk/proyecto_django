from django.contrib import admin
from django.urls import path
from Paginas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('formulario/', views.formulario, name='formulario'),
    path('redireccionamiento/', views.redireccionamiento, name='redireccionamiento'),
    path('calculadora/', views.calculadora, name='calculadora'),
    path("imagenes/", views.imagenes, name="imagenes"),
    path("imagenes/eliminar/<int:id>/", views.eliminar_imagen, name="eliminar_imagen"),
    path('error/', views.provocar_error),
    path('hola/', views.hola, name='hola'),

    path("crud/", views.crud, name="crud"),

    path("api/registros/", views.api_registros),
    path("api/crear/", views.api_crear),
    path("api/editar/<int:id>/", views.api_editar),
    path("api/eliminar/<int:id>/", views.api_eliminar),

]

from django.conf.urls import handler404, handler500

handler404 = 'Paginas.views.error_view'
handler500 = 'Paginas.views.error_view'
handler403 = 'Paginas.views.error_view'
handler400 = 'Paginas.views.error_view'
