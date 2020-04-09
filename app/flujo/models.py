from django.db import models
from home.models import Pregunta
from .types import FLUJO_FIN, FLUJO_INICIO, FLUJO_NORMAL

# Create your models here.
class Flujo(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name="pregunta_de_flujo", on_delete=models.CASCADE)

    FLUJO_OPCIONES = (
        (FLUJO_INICIO, "Inicio del Flujo"),
        (FLUJO_NORMAL, "Flujo normal"),
        (FLUJO_FIN, "Termina la encuesta")
    )
    tipo_flujo = models.CharField(max_length = 20, choices = FLUJO_OPCIONES)

    FIN_SECCION_OPCIONES = (
        (1, "Ultima pregunta de la seccion"),
        (0, "Mostrar siguiente pregunta en misma seccion")
    )
    fin_de_seccion = models.IntegerField(default=0, choices = FIN_SECCION_OPCIONES)

    ES_CONDICIONAL_OPCIONES = (
        (1, "Es una pregunta condicional. Automáticamente se convierte en final de seccioón"),
        (0, "No es una pregunta condicional")
    )
    es_condicional = models.IntegerField(default=0, choices=ES_CONDICIONAL_OPCIONES)

    siguiente_pregunta_en_flujo = models.ForeignKey('self', related_name="pregunta_siguiente", on_delete=models.CASCADE, blank=True, null=True)
    siguiente_pregunta_en_flujo_negativo = models.ForeignKey('self', related_name="pregunta_siguiente_flujo_negativo", on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.es_condicional == 1:
            self.fin_de_seccion = 1
        super(Flujo, self).save()

class Proceso(models.Model):
    flujo_actual = models.ForeignKey(Flujo, related_name="flujo_actual", on_delete=models.CASCADE, blank=True, null=True)