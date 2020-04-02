from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Pregunta(models.Model):
    pregunta_texto = models.CharField(max_length=250)
    pub_date = models.DateTimeField('fecha publicacion')
    estado = models.IntegerField(default=1)
    def __str__(self):
        return self.pregunta_texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name="pregunta", on_delete=models.CASCADE)
    opcion_texto = models.CharField(max_length = 200)
    orden = models.IntegerField(default=0)
    estado = models.IntegerField(default=1)
    def __str__(self):
        return self.opcion_texto

class Respuesta(models.Model):
    opcion = models.ForeignKey(Opcion, related_name="opcion", on_delete=models.CASCADE)
    location = models.PointField(geography=True, default=Point(0.0,0.0))
    fecha_creacion = models.DateTimeField('fecha creacion')
