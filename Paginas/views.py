from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Registro
import requests

# Página principal
def home(request):
    return render(request, 'home.html')

# Formulario con reCAPTCHA
def formulario(request):
    return render(request, 'formulario.html', {
        'site_key': settings.RECAPTCHA_SITE_KEY
    })

# Guardar datos
def guardar(request):
    if request.method == 'POST':

        recaptcha_response = request.POST.get('g-recaptcha-response')

        if not recaptcha_response:
            return HttpResponse("❌ No marcaste el reCAPTCHA")

        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }

        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data
        )

        result = r.json()

        if not result.get('success'):
            return HttpResponse(f"❌ reCAPTCHA inválido: {result}")

        Registro.objects.create(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion')
        )

        return HttpResponse("✅ Guardado en la base de datos")

def error_view(request, exception=None):
    return render(request, 'error.html', status=500)

def redireccionamiento(request):
    return render(request, 'redireccionamiento.html')

