from django.conf.urls import url
from GE.api_service.views.Users import views

urlpatterns = [
    url(r'^registros/$', views.registros),
    url(r'^atencion_masiva/$', views.atencion_masiva),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.registers_detail),
    url(r'^user_pin/(?P<pk>[0-9]+)/$', views.user_pin),
    url(r'^crear_turno/$', views.crear_turno),
    url(r'^crear_registro/$', views.crear_registro),
    url(r'^consulta_estado/$', views.consulta_estado),
    url(r'^actualiza_registro/(?P<id>[0-9]+)/$', views.actualiza_registro),
    url(r'^atencion_prioritaria/$', views.atencion_prioritaria),
    url(r'^visualizador/$', views.visualizador),
    url(r'^promedios/$', views.promedios),
    url(r'^get_promociones/$', views.get_promociones),
    url(r'^agregar_promociones/$', views.agregar_promociones),
    url(r'^seleccionar_promocion/$', views.seleccionar_promocion),
    url(r'^eliminar_promocion/$', views.delete_promociones),
    url(r'^get_promociones_visualizador/$', views.get_promociones_visualizador),
    url(r'^agregar_promociones_visualizador/$', views.agregar_promociones_visualizador),
    url(r'^eliminar_promocion_visualizador/$', views.delete_promociones_visualizador),
    url(r'^atenciones/$', views.atenciones),
    url(r'^usuarios/$', views.usuarios),
    url(r'^alertas/$', views.alertas)
]
