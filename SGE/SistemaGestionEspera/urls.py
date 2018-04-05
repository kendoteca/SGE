"""SistemaGestionEspera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from GE import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^totem/$', views.totem, name="totem"),
    url(r'^visualizador/$', views.visualizador, name="visualizador"),
    url(r'^data/$', views.data, name="data"),
    url(r'^configurations/$', views.configurations, name="configurations"),
    url(r'^final/$', views.final, name="final"),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^usuarios-admin/$', views.usuarios_admin, name='usuarios-admin'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^registros/$', views.registros, name='registros'),
    url(r'^personas/$', views.personas, name='personas'),
    url(r'^alertas/$', views.alertas, name='alertas'),
    url(r'^promociones/$', views.promociones, name='promociones'),
    url(r'^promociones_visualizador/$', views.promociones_visualizador, name='promociones-visualizador'),
    url(r'^prueba/$', views.prueba, name='prueba'),
    url(r'^api/', include('GE.api_service.api_urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
