from django.contrib import admin
from .models import Pregunta, Opcion, Respuesta

admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(Respuesta)

