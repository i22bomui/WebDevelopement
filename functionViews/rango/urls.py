from django.conf.urls import patterns, url
from rango import views

app_name = 'rango'	#Hay que ponerlo para dar/comprobar los permisos de un usuario

urlpatterns = [

	url(r'^$', views.index, name = 'index'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/$', views.page, name='page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/edit_page/$', views.edit_page, name='edit_page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/delete_page/$', views.delete_page, name='delete_page'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^restricted/$', views.restricted, name='restricted'),



]

#En la regex, \w busca cualquier caracter alfanumerico
