from django.urls import path
from . import views
from .views import RespuestasView
app_name = 'home'

urlpatterns=[
    path('', views.home, name='home'),
    path('respuesta', RespuestasView.as_view(), name="respuesta_view"),
]
