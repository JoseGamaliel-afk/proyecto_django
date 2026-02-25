from django.db import models
from django.utils import timezone 

class Registro(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.nombre
 
 

class Imagen(models.Model):
    titulo = models.CharField(max_length=100)
    imagen_url = models.URLField()
    public_id = models.CharField(max_length=200)
    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
