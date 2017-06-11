from django.conf.urls import url
from GE.api_service.views.Users import views

urlpatterns = [
    url(r'^snippets/$', views.rgisters_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.registers_detail),
    url(r'^user_pin/(?P<pk>[0-9]+)/$', views.user_pin),
]