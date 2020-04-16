from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils import timezone

class Pregunta(models.Model):
    pregunta_texto = models.CharField(max_length=250)
    pub_date = models.DateTimeField('fecha publicacion')
    estado = models.IntegerField(default=1)

    INPUT_CHOICES = (
        ("radio", "Respuesta unica"),
        ("checkbox", "Multiples respuestas"),
        ("email", "Correo electronico"),
        ("tel", "Telefono")
    )
    tipo_input = models.CharField(max_length = 20, choices = INPUT_CHOICES)

    @property
    def opciones(self):
        return list(Opcion.objects.filter(pregunta=self.pk).values("id", "opcion_texto"))

    def __str__(self):
        return self.pregunta_texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name="pregunta", on_delete=models.CASCADE)
    opcion_texto = models.CharField(max_length = 200)
    orden = models.IntegerField(default=0)
    estado = models.IntegerField(default=1)
    es_positiva = models.IntegerField(default=0)
    def __str__(self):
        return self.opcion_texto

class Respuesta(models.Model):
    opcion = models.ForeignKey(Opcion, related_name="opcion", on_delete=models.CASCADE)
    location = models.PointField(geography=True, default=Point(0.0,0.0))
    fecha_creacion = models.DateTimeField('fecha creacion', default=timezone.now)
    hora_encuesta_iniciada = models.DateTimeField('fecha inicio encuesta', null=False, blank=False)

class DatosPersonales(models.Model):
    fecha_nacimiento = models.CharField(max_length=4, blank=False, null = False)
    GENERO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro")
    )
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    correo = models.CharField(max_length= 200, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha_creacion = models.DateTimeField('fecha creacion', default=timezone.now)
    hora_encuesta_iniciada = models.DateTimeField('fecha inicio encuesta', null=False, blank=False)
