from django.urls import path
from .views import IniciarFlujoView, EnviarRespuestasView, ObtenerPreguntasSiguientes
app_name = 'flujo'

urlpatterns=[
    path('iniciar_flujo', IniciarFlujoView.as_view(), name='iniciar_flujo'),
    path('enviar_respuestas', EnviarRespuestasView.as_view(), name='enviar_respuestas'),
    path('<int:pk>', ObtenerPreguntasSiguientes.as_view(), name='flujo_preguntas'),
]