from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView, TemplateView, FormView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import *
from .forms import *

# Pagina principal

class IndexView(TemplateView):


	template_name = 'rango/index.html'


	def get_context_data(self, **kwargs):

		context = super(IndexView, self).get_context_data(**kwargs)

		context['categories_by_likes'] = Category.objects.order_by('-views')[:5]
		context['pages_by_views'] = Page.objects.order_by('-views')[:5]

		return context

# ------------------------------------------------------------------------- #

# Se usa ListView porque el queryset va a devolver una lista y no solo un objeto

class CategoryView(ListView):


	context_object_name = 'page_list'
	template_name = 'rango/category.html'


	def get_queryset(self):

		self.category = get_object_or_404(Category, slug = self.kwargs['category_name_slug'])
		return Page.objects.filter(category = self.category)

	def get_context_data(self, **kwargs):

		context = super(CategoryView, self).get_context_data(**kwargs)

		context['category'] = self.category
		return context


# Se crea el formulario sobrecargando la clase CreateView

class CategoryCreate(CreateView):

	template_name = 'rango/add_category.html'
#	formClass = CategoryForm
	success_url = '/rango/'

	model = Category
	fields = ['name']



# ------------------------------------------------------------------------- #

#Vista para las paginas en detalle de las diferentes paginas

class PageView(DetailView):

	context_object_name = 'page_detail'
	template_name = 'rango/page.html'

	def get_object(self):

		return get_object_or_404(Page, slug = self.kwargs['page_name_slug'])

	def get_context_data(self, **kwargs):

		context = super(PageView, self).get_context_data(**kwargs)

		context['category'] = get_object_or_404(Category, slug = self.kwargs['category_name_slug'])
		return context


#Clase que anadira una nueva pagina dentro de una categoria a traves de un formulario


class PageCreate(CreateView):


	template_name = 'rango/add_page.html'

	model = Page
	fields = ['title', 'url']

	# Funcion que usaremos unicamente para comprobar si el usuario tiene los permisos necesarios
	@method_decorator(permission_required('rango.add_page', login_url='/rango/login/'))
	def dispatch(self, *args, **kwargs):
		return super(PageCreate, self).dispatch(*args,**kwargs)

	# Funcion que se ejecutara unicamente si el formulario dado es valido, en el guardaremos el mismo
	def form_valid(self, form, **kwargs):

		page = form.save(commit = False)
		page.category = get_object_or_404(Category, slug = self.kwargs['category_name_slug'])
		page.views = 0

		page.save()
		return super(PageCreate, self).form_valid(form, **kwargs)


	def get_context_data(self, **kwargs):

		context = super(PageCreate, self).get_context_data(**kwargs)

		context['category'] = get_object_or_404(Category, slug = self.kwargs['category_name_slug'])
		return context

	# Definimos la URL a la que se redigira si es valido el formulario (Usado para devolver argumentos)
	def get_success_url(self):

		return reverse_lazy('category', kwargs={'category_name_slug': self.kwargs['category_name_slug']})





# Clase que editara un pagina ya existente si el usuario esta registrado

#Para el decorador, los permisos se deben especificar de la siguiente forma: <app_label>.<permiso>_<modelo>
#Teniendo que estar el nombre del modelo en minusculas


class PageUpdate(UpdateView):

	template_name = 'rango/edit_page.html'
	slug_url_kwarg = 'page_name_slug'		#Si no se especifica el nombre de la pk o el slug peta

	model = Page
	fields = ['title', 'url']

	# Funcion que usaremos unicamente para comprobar si el usuario tiene los permisos necesarios
	@method_decorator(permission_required('rango.change_page', login_url='/rango/login/'))
	def dispatch(self, *args, **kwargs):
		return super(PageUpdate, self).dispatch(*args,**kwargs)

	# Funcion que se ejecutara unicamente si el formulario dado es valido, en el guardaremos el mismo
	def form_valid(self, form, **kwargs):

		form.save()
		return super(PageUpdate, self).form_valid(form, **kwargs)


	def get_context_data(self, **kwargs):

		context = super(PageUpdate, self).get_context_data(**kwargs)

		context['category_name_slug'] = self.kwargs['category_name_slug']
		context['page_name_slug'] = self.kwargs['page_name_slug']
		return context

	# Definimos la URL a la que se redigira si es valido el formulario (Usado para devolver argumentos)
	def get_success_url(self):

		return reverse_lazy('category', kwargs={'category_name_slug': self.kwargs['category_name_slug']})




class PageDelete(DeleteView):

	template_name = 'rango/delete_page.html'
	slug_url_kwarg = 'page_name_slug'		#Si no se especifica el nombre de la pk o el slug peta
	model = Page


	@method_decorator(permission_required('rango.delete_page', login_url='/rango/login/'))
	def dispatch(self, *args, **kwargs):
		return super(PageDelete, self).dispatch(*args,**kwargs)


	def get_success_url(self):

		return reverse_lazy('category', kwargs={'category_name_slug': self.kwargs['category_name_slug']})


# ------------------------------------------------------------------------- #


class RegisterView(FormView):


	form_class = UserForm
	template_name = 'rango/register.html'
	success_url = '/rango/'

	registered = False

	def form_valid(self, form):


		user = form.save(commit = False)
		user.set_password(user.password)

		user.save()

		registered = True
		return super(RegisterView, self).form_valid(form)



# ------------------------------------------------------------------------- #


class LoginView(FormView):

	success_url = '/rango/'
	form_class = AuthenticationForm
	template_name = 'rango/login.html'

	def form_valid(self, form):

		login(self.request, form.get_user())
		return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):


	url = '/rango/'	#En RedirectView la url a la que se redirige se especifica asi

	@method_decorator(login_required(login_url = '/rango/login/'))
	def get(self, request, *args, **kwargs):

		logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)



# ------------------------------------------------------------------------- #

def about(request):

	return render(request, 'rango/about.html')


# ------------------------------------------------------------------------- #

#*	En el caso de que un usuario no logueado intente acceder			*#
#*	habremos de definir una accion a realizar, siendo la redireccion	*#
#*	el escogido. Para ello tendremos que definir en settings.py la 		*#
#*	direccion del servidor a la que se redirigira mediante LOGIN_URL	*#



@login_required
def restricted(request):

	return HttpResponse("Since you're logged in, you can see this")







