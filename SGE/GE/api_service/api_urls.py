from django.conf.urls import url
from GE.api_service.views.Users import views

urlpatterns = [
    url(r'^registros/$', views.registros),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.registers_detail),
    url(r'^user_pin/(?P<pk>[0-9]+)/$', views.user_pin),
    url(r'^crear_turno/$', views.crear_turno),
    url(r'^crear_registro/$', views.crear_registro),
    url(r'^consulta_estado/$', views.consulta_estado),
    url(r'^actualiza_registro/(?P<id>[0-9]+)/$', views.actualiza_registro),
    url(r'^atencion_prioritaria/$', views.atencion_prioritaria),
    url(r'^visualizador/$', views.visualizador),
    url(r'^promedios/$', views.promedios),
    url(r'^atenciones/$', views.atenciones),
    url(r'^usuarios/$', views.usuarios),
    url(r'^alertas/$', views.alertas)
]
