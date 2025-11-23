from PIL import Image
import os
from django.conf import settings

def procesar_foto_perfil(instance):
    """
    - Recorta la imagen a cuadrado
    - Reduce tamaño
    - Elimina la imagen anterior
    """
    if not instance.foto:
        return

    foto_path = instance.foto.path

    # Eliminar imagen anterior: ejemplo simple
    try:
        cls = instance.__class__
        old = cls.objects.get(pk=instance.pk)
        if old.foto and old.foto.path != foto_path and os.path.exists(old.foto.path):
            os.remove(old.foto.path)
    except cls.DoesNotExist:
        pass

    img = Image.open(foto_path)
    # Recorte cuadrado simple
    min_size = min(img.size)
    left = (img.width - min_size) / 2
    top = (img.height - min_size) / 2
    right = (img.width + min_size) / 2
    bottom = (img.height + min_size) / 2
    img = img.crop((left, top, right, bottom))

    # Reducción de tamaño
    img.thumbnail((400, 400))

    img.save(foto_path, optimize=True, quality=80)

def compress_image(image):
    """
    Comprime la imagen
    """
    if not image:
        return

    img = Image.open(image)
    img.thumbnail((400, 400))
    img.save(image, optimize=True, quality=80)

def procesar_foto(ruta):
    """
    Recorta y optimiza una imagen
    """
    img = Image.open(ruta)

    # convertir a cuadrado
    min_size = min(img.size)
    left = (img.width - min_size) / 2
    top = (img.height - min_size) / 2
    right = left + min_size
    bottom = top + min_size
    img = img.crop((left, top, right, bottom))

    # reducir tamaño
    img.thumbnail((400, 400))

    img.save(ruta, optimize=True, quality=80)
