from django.contrib import admin
from django.urls import path
from Paginas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('formulario/', views.formulario, name='formulario'),
    path('guardar/', views.guardar, name='guardar'),
   path('redireccionamiento/', views.redireccionamiento, name='redireccionamiento'),

]

from django.conf.urls import handler404, handler500

handler404 = 'Paginas.views.error_view'
handler500 = 'Paginas.views.error_view'
handler403 = 'Paginas.views.error_view'
handler400 = 'Paginas.views.error_view'
