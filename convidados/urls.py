from django.urls import path
from . import views 

urlpatterns = [
    path('', view=views.detatalhe_convidado, name='convidados'),
    path(route='responder_presenca', view=views.responder_presenca, name='responder_presenca'),
    path(route='reservar_presente/<int:id>', view=views.reservar_presente, name='reservar_presente'),
    path(route='adicionar_acompanhantes', view=views.adicionar_acompanhantes, name='adicionar_acompanhantes'),
]
