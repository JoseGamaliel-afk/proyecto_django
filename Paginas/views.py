from django.shortcuts import render, redirect
from django.conf import settings
from django.db import DataError
from django.contrib import messages
from django.http import HttpResponse

from datetime import date
import requests
import cloudinary.uploader

from .models import Registro, Imagen

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



# ==================== HOME ====================

def home(request):
    return render(request, 'home.html', {
        'breadcrumbs': []
    })


# ==================== REDIRECCIONAMIENTO ====================

def redireccionamiento(request):
    return render(request, 'redireccionamiento.html', {
        'breadcrumbs': [{"label": "Error", "url": None}]
    })


# ==================== FORMULARIO ====================

def formulario(request):

    MAX_NOMBRE = 50
    MAX_EMAIL = 254

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        descripcion = request.POST.get('descripcion', '').strip()
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # -------- VALIDACIONES BACKEND --------
        if not nombre or len(nombre) < 4:
            messages.error(request, "❌ El nombre debe tener al menos 4 caracteres")

        elif len(nombre) > MAX_NOMBRE:
            messages.error(request, "❌ El nombre es demasiado largo")

        elif not email:
            messages.error(request, "❌ El correo es obligatorio")

        elif len(email) > MAX_EMAIL:
            messages.error(request, "❌ El correo es demasiado largo")

        elif Registro.objects.filter(email=email).exists():
            messages.error(request, "❌ Este correo ya está registrado")

        elif fecha_nacimiento and date.fromisoformat(fecha_nacimiento) > date.today():
            messages.error(request, "❌ La fecha no puede ser futura")

        elif not recaptcha_response:
            messages.error(request, "❌ Debes marcar el reCAPTCHA")

        else:
            # -------- VALIDAR reCAPTCHA --------
            response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": recaptcha_response
                }
            ).json()

            if not response.get("success"):
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
                    return redirect('formulario')  # 🔥 PRG
                except DataError:
                    messages.error(request, "❌ Error al guardar los datos")

    registros = Registro.objects.order_by('-id')

    return render(request, 'formulario.html', {
        'registros': registros,
        'site_key': settings.RECAPTCHA_SITE_KEY
    })


# ==================== CALCULADORA ====================
from django.shortcuts import render

def calculadora(request):
    resultado = None

    if request.method == "POST":
        try:
            n1 = float(request.POST.get('n1', 0))
            n2 = float(request.POST.get('n2', 0))
            operacion = request.POST.get('operacion')

            if operacion == 'sumar':
                resultado = n1 + n2

            elif operacion == 'restar':
                resultado = n1 - n2

            elif operacion == 'multiplicar':
                resultado = n1 * n2

            elif operacion == 'dividir':
                resultado = "❌ No se puede dividir entre 0" if n2 == 0 else n1 / n2

            elif operacion == 'potencia':
                resultado = n1 ** n2

            else:
                resultado = "❌ Operación no válida"

        except ValueError:
            resultado = "❌ Valores inválidos"

    return render(request, 'calculadora.html', {
        'breadcrumbs': [{"label": "Calculadora", "url": None}],
        'resultado': resultado
    })

# ==================== CARRUSEL ====================

def carrusel(request):
    imagenes = [f"https://picsum.photos/id/{i}/800/400" for i in range(10, 15)]

    return render(request, 'carrusel.html', {
        'breadcrumbs': [{"label": "Carrusel", "url": None}],
        'imagenes': imagenes
    })


# ==================== GALERÍA (CLOUDINARY) ====================

def imagenes(request):

    if request.method == "POST" and request.FILES.get("imagen"):
        archivo = request.FILES["imagen"]

        # -------- VALIDAR QUE SEA IMAGEN --------
        tipos_permitidos = ["image/jpeg", "image/png", "image/webp", "image/gif"]
        extensiones_permitidas = [".jpg", ".jpeg", ".png", ".webp", ".gif"]

        if archivo.content_type not in tipos_permitidos:
            messages.error(request, "❌ El archivo debe ser una imagen válida")
            return redirect("imagenes")

        if not archivo.name.lower().endswith(tuple(extensiones_permitidas)):
            messages.error(request, "❌ Extensión de imagen no permitida")
            return redirect("imagenes")

        # (opcional) tamaño máximo: 5MB
        if archivo.size > 5 * 1024 * 1024:
            messages.error(request, "❌ La imagen no puede pesar más de 5MB")
            return redirect("imagenes")

        # -------- SUBIR A CLOUDINARY --------
        resultado = cloudinary.uploader.upload(
            archivo,
            folder="galeria",
            resource_type="image"
        )

        Imagen.objects.create(
            titulo=request.POST.get("titulo", "Sin título"),
            imagen_url=resultado["secure_url"],
            public_id=resultado["public_id"]
        )

        messages.success(request, "✅ Imagen subida correctamente")
        return redirect("imagenes")

    imagenes = Imagen.objects.all().order_by("-id")
    total = imagenes.count()
    faltantes = 0 if total % 3 == 0 else 3 - (total % 3)

    return render(request, "imagenes.html", {
        "imagenes": imagenes,
        "breadcrumbs": [{"label": "Galería", "url": None}],
        "faltantes": faltantes
    })

# ==================== ELIMINAR IMAGEN ====================

def eliminar_imagen(request, id):
    try:
        imagen = Imagen.objects.get(id=id)
        cloudinary.uploader.destroy(imagen.public_id)
        imagen.delete()
        messages.success(request, "🗑️ Imagen eliminada")
    except Imagen.DoesNotExist:
        messages.error(request, "❌ La imagen no existe")

    return redirect("imagenes")


# ==================== ERRORES ====================

def error_view(request, exception=None):
    return render(request, 'error.html', {
        'breadcrumbs': [{"label": "Error", "url": None}]
    }, status=500)


def trigger_error(request):
    raise Exception("Error intencional")


def provocar_error(request):
    x = 1 / 0  # 💥 Error real


# ==================== TEST ====================

def hola(request):
    return render(request, 'hola.html', {
        'breadcrumbs': [
            {"label": "Home", "url": "home"},
            {"label": "Hola", "url": None}
        ]
    })
# ==================== CRUD CON FETCH API ====================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from .models import Registro
import json


# ---------- Vista que carga la página ----------
def crud(request):
    return render(request, "crud.html")


# ---------- READ ----------
def api_registros(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    registros = Registro.objects.all().order_by("-fecha_creacion")

    data = list(registros.values(
        "id",
        "nombre",
        "email",
        "telefono",
        "descripcion",
        "fecha_nacimiento",
        "fecha_creacion"
    ))

    return JsonResponse(data, safe=False)


# ---------- CREATE ----------
@csrf_exempt
def api_crear(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        registro = Registro.objects.create(
            nombre=data.get("nombre", "").strip(),
            email=data.get("email") or None,
            telefono=data.get("telefono") or None,
            descripcion=data.get("descripcion", "").strip(),
            fecha_nacimiento=data.get("fecha_nacimiento") or None
        )

        return JsonResponse(
            {"mensaje": "Creado correctamente", "id": registro.id},
            status=201
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---------- UPDATE ----------
@csrf_exempt
def api_editar(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        registro = get_object_or_404(Registro, id=id)

        registro.nombre = data.get("nombre", registro.nombre)
        registro.email = data.get("email", registro.email)
        registro.telefono = data.get("telefono", registro.telefono)
        registro.descripcion = data.get("descripcion", registro.descripcion)
        registro.fecha_nacimiento = data.get(
            "fecha_nacimiento",
            registro.fecha_nacimiento
        )

        registro.save()

        return JsonResponse({"mensaje": "Actualizado correctamente"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---------- DELETE ----------
@csrf_exempt
def api_eliminar(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    registro = get_object_or_404(Registro, id=id)
    registro.delete()

    return JsonResponse({"mensaje": "Eliminado correctamente"})

