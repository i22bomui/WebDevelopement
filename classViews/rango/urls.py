from django.conf.urls import patterns, url
from rango import views
from rango.views import IndexView, CategoryView, PageView, CategoryCreate, PageCreate, PageUpdate
from rango.views import PageDelete, RegisterView, LoginView, LogoutView

app_name = 'rango'	#Hay que ponerlo para dar/comprobar los permisos de un usuario

urlpatterns = [

	url(r'^$', IndexView.as_view(), name = 'index'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^add_category/$', CategoryCreate.as_view(), name='add_category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', CategoryView.as_view(), name='category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', PageCreate.as_view(), name='add_page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/$', PageView.as_view(), name='page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/edit_page/$', PageUpdate.as_view(), name='edit_page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/delete_page/$', PageDelete.as_view(), name='delete_page'),
	url(r'^register/$', RegisterView.as_view(), name='register'),
	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
	url(r'^restricted/$', views.restricted, name='restricted'),



]

#En la regex, \w busca cualquier caracter alfanumerico
