from django.urls import path
from .views import IniciarFlujoView
app_name = 'flujo'

urlpatterns=[
    path('iniciar_flujo', IniciarFlujoView.as_view(), name='iniciar_flujo'),
]