from django.urls import path
from . import views
from .views import RespuestasView, PreguntasView, DatosPersonalesView
app_name = 'home'

urlpatterns=[
    path('', views.home, name='home'),
    path('encuesta', views.encuesta, name='encuesta'),
    path('respuesta', RespuestasView.as_view(), name="respuesta_view"),
    path('preguntas', PreguntasView.as_view(), name="preguntas_view"),
    path('datos_personales', DatosPersonalesView.as_view(), name="datos_personales_view"),
]
