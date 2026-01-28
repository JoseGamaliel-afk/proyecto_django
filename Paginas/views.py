from django.shortcuts import render, redirect
from django.conf import settings
from django.db import DataError
from django.contrib import messages
from .models import Registro, Imagen
import requests
from datetime import date
import cloudinary.uploader


# -------------------- HOME --------------------

def home(request):
    return render(request, 'home.html', {
        'breadcrumbs': []
    })


# -------------------- REDIRECCIONAMIENTO --------------------

def redireccionamiento(request):
    return render(request, 'redireccionamiento.html', {
        'breadcrumbs': [{"label": "Error", "url": None}]
    })


# -------------------- FORMULARIO + VALIDACIONES + reCAPTCHA --------------------

def formulario(request):

    breadcrumbs = [{"label": "Formulario", "url": None}]

    MAX_NOMBRE = 50
    MAX_EMAIL = 254
    MAX_TELEFONO = 15
    MAX_DESCRIPCION = 500

    if request.method == 'POST':

        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        descripcion = request.POST.get('descripcion', '').strip()
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # -------- VALIDACIONES --------

        if not nombre or len(nombre) < 3:
            messages.error(request, "❌ El nombre debe tener al menos 3 caracteres")

        elif len(nombre) > MAX_NOMBRE:
            messages.error(request, f"❌ Máximo {MAX_NOMBRE} caracteres permitidos en el nombre")

        elif not email:
            messages.error(request, "❌ El email es obligatorio")

        elif len(email) > MAX_EMAIL:
            messages.error(request, "❌ El email es demasiado largo")

        elif Registro.objects.filter(email=email).exists():
            messages.error(request, "❌ Este email ya está registrado")

        elif telefono and (not telefono.isdigit() or len(telefono) > MAX_TELEFONO):
            messages.error(request, "❌ El teléfono es inválido")

        elif descripcion and len(descripcion) > MAX_DESCRIPCION:
            messages.error(request, f"❌ Máximo {MAX_DESCRIPCION} caracteres permitidos")

        elif fecha_nacimiento and date.fromisoformat(fecha_nacimiento) > date.today():
            messages.error(request, "❌ La fecha de nacimiento no puede ser futura")

        elif not recaptcha_response:
            messages.error(request, "❌ Debes marcar el reCAPTCHA")

        else:
            # -------- VALIDAR reCAPTCHA --------
            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data={
                    'secret': settings.RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
            )

            if not response.json().get('success'):
                messages.error(request, "❌ reCAPTCHA inválido")
            else:
                try:
                    Registro.objects.create(
                        nombre=nombre,
                        email=email,
                        telefono=telefono,
                        fecha_nacimiento=fecha_nacimiento,
                        descripcion=descripcion
                    )
                    messages.success(request, "✅ Registro guardado correctamente")
                    return redirect('formulario')  # 🔑 PRG

                except DataError:
                    messages.error(request, "❌ Error: datos demasiado largos")

    registros = Registro.objects.order_by('-id')

    return render(request, 'formulario.html', {
        'breadcrumbs': breadcrumbs,
        'site_key': settings.RECAPTCHA_SITE_KEY,
        'registros': registros
    })


# -------------------- CALCULADORA --------------------

def calculadora(request):

    resultado = None

    if request.method == "POST":
        try:
            n1 = float(request.POST.get('n1', 0))
            n2 = float(request.POST.get('n2', 0))
            operacion = request.POST.get('operacion')

            if operacion == 'sumar':
                resultado = n1 + n2
            elif operacion == 'dividir':
                resultado = "❌ No se puede dividir entre 0" if n2 == 0 else n1 / n2

        except ValueError:
            resultado = "❌ Valores inválidos"

    return render(request, 'calculadora.html', {
        'breadcrumbs': [{"label": "Calculadora", "url": None}],
        'resultado': resultado
    })


# -------------------- CARRUSEL --------------------

def carrusel(request):
    imagenes = [f"https://picsum.photos/id/{i}/800/400" for i in range(10, 15)]

    return render(request, 'carrusel.html', {
        'breadcrumbs': [{"label": "Carrusel", "url": None}],
        'imagenes': imagenes
    })


# -------------------- IMÁGENES (Subida + Galería + Carrusel) --------------------

def imagenes(request):

    if request.method == "POST" and request.FILES.get("imagen"):
        archivo = request.FILES["imagen"]

        resultado = cloudinary.uploader.upload(archivo, folder="galeria")

        Imagen.objects.create(
            titulo=request.POST.get("titulo", "Sin título"),
            imagen_url=resultado["secure_url"],
            public_id=resultado["public_id"]
        )

        messages.success(request, "✅ Imagen subida correctamente")
        return redirect("imagenes")  # 🔑 PRG

    imagenes = Imagen.objects.all().order_by("-id")

    return render(request, "imagenes.html", {
        "imagenes": imagenes,
        "breadcrumbs": [{"label": "Galería", "url": None}]
    })


# -------------------- ELIMINAR IMAGEN --------------------

def eliminar_imagen(request, id):
    try:
        imagen = Imagen.objects.get(id=id)
        cloudinary.uploader.destroy(imagen.public_id)
        imagen.delete()
        messages.success(request, "🗑 Imagen eliminada")
    except Imagen.DoesNotExist:
        messages.error(request, "❌ La imagen no existe")

    return redirect("imagenes")


# -------------------- ERRORES --------------------

def error_view(request, exception=None):
    return render(
        request,
        'error.html',
        {'breadcrumbs': [{"label": "Error", "url": None}]},
        status=500
    )


def trigger_error(request):
    raise Exception("Error intencional")


def provocar_error(request):
    x = 1 / 0  # 💥 error real

def hola(request):
    return render(request, 'hola.html')
