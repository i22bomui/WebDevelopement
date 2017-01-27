from django.conf.urls import patterns, url
from entregas import views
from entregas.views import DestinatarioListView, DestinatarioCreateView, DestinatarioView
from entregas.views import PaqueteListView, PaqueteView, PaqueteCreateView, PaqueteUpdateView, PaqueteDeleteView
from entregas.views import RutaListView, RutaView, RutaCreateView, RutaUpdateView, RutaDeleteView

from django.views.generic import TemplateView

app_name = 'entregas'

urlpatterns = [


	url(r'^$', TemplateView.as_view(template_name = 'entregas/index.html'), name = 'index'),
	url(r'^destinatario/$', DestinatarioListView.as_view(), name = 'list_destinatario'),
	url(r'^destinatario/add_destinatario/$', DestinatarioCreateView.as_view(), name = 'add_destinatario'),
	url(r'^destinatario/(?P<destinatario_id>\d+)/$', DestinatarioView.as_view(), name = 'detail_destinatario'),

	url(r'^paquete/$', PaqueteListView.as_view(), name = 'list_paquete'),
	url(r'^paquete/add_paquete/$', PaqueteCreateView.as_view(), name = 'add_paquete'),
	url(r'^paquete/(?P<paquete_id>\d+)/$', PaqueteView.as_view(), name = 'detail_paquete'),
	url(r'^paquete/(?P<paquete_id>\d+)/change_paquete/$', PaqueteUpdateView.as_view(), name = 'change_paquete'),
	url(r'^paquete/(?P<paquete_id>\d+)/delete_paquete/$', PaqueteDeleteView.as_view(), name = 'delete_paquete'),

	url(r'^ruta/$', RutaListView.as_view(), name = 'list_ruta'),
	url(r'^ruta/add_paquete/$', RutaCreateView.as_view(), name = 'add_ruta'),
	url(r'^ruta/(?P<ruta_id>\d+)/$', RutaView.as_view(), name = 'detail_ruta'),
	url(r'^ruta/(?P<ruta_id>\d+)/change_ruta/$', RutaUpdateView.as_view(), name = 'change_ruta'),
	url(r'^ruta/(?P<ruta_id>\d+)/delete_ruta/$', RutaDeleteView.as_view(), name = 'delete_ruta'),

	url(r'^login/$', views.user_login, name = 'login'),
	url(r'^logout/$', views.user_logout, name = 'logout')



]
