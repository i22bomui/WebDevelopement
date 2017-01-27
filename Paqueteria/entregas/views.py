from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from entregas.models import *
#from entregas.forms import *


class DestinatarioListView(ListView):

	template_name = 'entregas/list_destinatario.html'
	context_object_name = 'list_destinatario'
	model = Destinatario

class DestinatarioCreateView(CreateView):

	model = Destinatario
	fields = ['direccion','ciudad','distancia']

	template_name = 'entregas/add_destinatario.html'
	success_url = '/destinatario/'

	@method_decorator(login_required(login_url = '/login/'))
	def dispatch(self, *args, **kwargs):
		return super(DestinatarioCreateView, self).dispatch(*args, **kwargs)


class DestinatarioView(DetailView):

	context_object_name = 'destinatario'
	model = Destinatario

	template_name = 'entregas/detail_destinatario.html'

	pk_url_kwarg = 'destinatario_id'


#	Al definir pk_url_kwarg esta funcion no es necesario sobrecargarla
#
#	def get_object(self):
#
#		return get_object_or_404(Destinatario, pk = )

# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #


class PaqueteListView(ListView):

	template_name = 'entregas/list_paquete.html'
	context_object_name = 'list_paquete'
	model = Paquete


class PaqueteView(DetailView):

	context_object_name = 'paquete'
	model = Paquete

	template_name = 'entregas/detail_paquete.html'

	pk_url_kwarg = 'paquete_id'

	def get_context_data(self, **kwargs):

		context = super(PaqueteView, self).get_context_data(**kwargs)

		context['destinatario'] = Paquete.objects.get(pk = self.kwargs['paquete_id']).destinatario
		return context


class PaqueteCreateView(CreateView):

	model = Paquete
	fields = ['contenido','valor','destinatario', 'ruta']

	template_name = 'entregas/add_paquete.html'
	success_url = '/paquete/'

	@method_decorator(login_required(login_url = '/login/'))
	def dispatch(self, *args, **kwargs):
		return super(PaqueteCreateView, self).dispatch(*args, **kwargs)


class PaqueteUpdateView(UpdateView):

	model = Paquete
	template_name = 'entregas/change_paquete.html'
	pk_url_kwarg = 'paquete_id'

	fields = ['contenido','valor','destinatario', 'ruta']


	def form_valid(self, form, **kwargs):

		form.save()
		return super(PaqueteUpdateView, self).form_valid(form, **kwargs)

	def get_success_url(self):

		return reverse_lazy('detail_paquete', kwargs={'paquete_id': self.kwargs['paquete_id']})

	def get_context_data(self, **kwargs):

		context = super(PaqueteUpdateView, self).get_context_data(**kwargs)

		context['paquete_id'] = self.kwargs['paquete_id']
		return context

	@method_decorator(login_required(login_url = '/login/'))
	def dispatch(self, *args, **kwargs):
		return super(PaqueteUpdateView, self).dispatch(*args, **kwargs)


class PaqueteDeleteView(DeleteView):

	model = Paquete

	template_name = 'entregas/delete.html'
	success_url = '/paquete/'
	pk_url_kwarg = 'paquete_id'

	@method_decorator(login_required(login_url = '/login/'))
	def dispatch(self, *args, **kwargs):
		return super(PaqueteDeleteView, self).dispatch(*args, **kwargs)


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #




class RutaListView(ListView):

	template_name = 'entregas/list_ruta.html'
	context_object_name = 'list_ruta'
	model = Ruta


class RutaView(DetailView):

	context_object_name = 'ruta'
	model = Ruta

	template_name = 'entregas/detail_ruta.html'

	pk_url_kwarg = 'ruta_id'

	def get_context_data(self, **kwargs):

		context = super(RutaView, self).get_context_data(**kwargs)

		auxRuta = Ruta.objects.get(pk = self.kwargs['ruta_id'])
		context['list_paquete'] = Paquete.objects.filter(ruta = auxRuta)
		return context


class RutaCreateView(CreateView):

	model = Ruta
	fields = ['nombre']

	template_name = 'entregas/add_ruta.html'
	success_url = '/ruta/'

	@method_decorator(login_required(login_url = '/login/'))
	def dispatch(self, *args, **kwargs):
		return super(RutaCreateView, self).dispatch(*args, **kwargs)


class RutaUpdateView(UpdateView):

	model = Ruta
	template_name = 'entregas/change_ruta.html'
	pk_url_kwarg = 'ruta_id'

	fields = ['nombre']


	def form_valid(self, form, **kwargs):

		form.save()
		return super(RutaUpdateView, self).form_valid(form, **kwargs)

	def get_success_url(self):

		return reverse_lazy('detail_ruta', kwargs={'ruta_id': self.kwargs['ruta_id']})

	def get_context_data(self, **kwargs):

		context = super(RutaUpdateView, self).get_context_data(**kwargs)

		context['ruta_id'] = self.kwargs['ruta_id']
		return context

	@method_decorator(login_required(login_url = '/login/'))
	def dispatch(self, *args, **kwargs):
		return super(RutaUpdateView, self).dispatch(*args, **kwargs)


class RutaDeleteView(DeleteView):

	model = Ruta

	template_name = 'entregas/delete.html'
	success_url = '/ruta/'
	pk_url_kwarg = 'ruta_id'

	@method_decorator(login_required(login_url = '/login/'))
	def dispatch(self, *args, **kwargs):
		return super(RutaDeleteView, self).dispatch(*args, **kwargs)





# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #






def user_login(request):


	if request.method == "POST":

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:

			if user.is_active:

				login(request, user)
				return HttpResponseRedirect('/')

			else:

				return HttpResponse("Tu cuenta de Django esta deshabilitada")

		else:

			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied")

	else:

		return render(request, 'entregas/login.html', {})


def user_logout(request):


	logout(request)
	return HttpResponseRedirect('/')




























