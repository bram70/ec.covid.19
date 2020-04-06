from django.urls import path
from . import views
from .views import RespuestasView, PreguntasView
app_name = 'home'

urlpatterns=[
    path('', views.home, name='home'),
    path('respuesta', RespuestasView.as_view(), name="respuesta_view"),
    path('preguntas', PreguntasView.as_view(), name="preguntas_view"),
]
