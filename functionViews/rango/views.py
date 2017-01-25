from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from .models import *
from .forms import *

# Pagina principal

def index(request):

	context_dict = {}

	category_list_likes = Category.objects.order_by('-likes')[:5]	
	context_dict['categories_by_likes'] = category_list_likes

	pages_list_views = Page.objects.order_by('-views')[:5]
	context_dict['pages_by_views'] = pages_list_views

	return render(request, 'rango/index.html', context_dict)

# ------------------------------------------------------------------------- #

# Vista en detalle para las diferentes categorias

def category(request, category_name_slug):

	context_dict = {}

	try:

		category = Category.objects.get(slug=category_name_slug)

		category.views += 1
		category.save()

		context_dict['category_name'] = category.name

		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages

		context_dict['category'] = category
		context_dict['category_name_slug'] = category_name_slug

	except Category.DoesNotExist:
		pass

	return render(request, 'rango/category.html', context_dict)


#Clase que anadira una nueva categoria a traves de un formulario


#*	El metodo POST se utiliza en la plantilla add_category	mediante		*#
#*	el formulario. La primera llamada a esta funcion sera mediante un GET	*#
#*	(cuando clicamos en 'anhadir categoria'), por lo que se renderizara		*#
#*	la plantilla add_category, y tras rellenarla, vuelve a entrar a esta	*#
#*	vista, esta vez mediante un metodo POST con el formulario relleno		*#
#*																			*#
#*	Si el formulario es correcto se renderiza la pagina de inicio, sino 	*#
#*	se vuelve a mostrar la plantilla add_category con el mensaje de error 	*#

@login_required
def add_category(request):

	#A HTTP POST?
	if request.method == 'POST':

		form = CategoryForm(request.POST)

		#Have we been provided with a valid form?
		if form.is_valid():
			#Save the new category to the database
			form.save(commit=True)

			# Now call the index() view
			# The user will be shown the homepage
			return index(request)

		else:

			# The supplied form contained errors - just print them to the terminal
			print form.errors

	else:
		# If the request was not a POST, display the form to enter details
		form = CategoryForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any)
	return render(request, 'rango/add_category.html', {'form': form})



# ------------------------------------------------------------------------- #

#Vista para las paginas en detalle de las diferentes paginas

def page(request, category_name_slug, page_name_slug):

	context_dict = {}

	try:

		page = Page.objects.get(slug=page_name_slug)

		page.views += 1
		page.save()

		context_dict['title'] = page.title
		context_dict['url'] = page.url
		context_dict['category'] = page.category

		context_dict['page'] = page

	except Category.DoesNotExist:
		pass

	return render(request, 'rango/page.html', context_dict)


#Clase que anadira una nueva pagina dentro de una categoria a traves de un formulario

@login_required
def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug = category_name_slug)
	except Category.DoesNotExist:
		cat = None


	if request.method == 'POST':

		form = PageForm(request.POST)

		if form.is_valid():

			if cat:

				page = form.save(commit=False)
				page.category = cat
				page.views = 0 		# Esto hara que la pagina creada tenga siempre 0 visitas
				page.save()

				#Probably better to use a redirect here
				return category(request, category_name_slug)

		else:
			print form.errors

	else:
		form = PageForm()


	context_dict = {'form': form, 'category': cat}

	return render(request, 'rango/add_page.html', context_dict)


# Clase que editara un pagina ya existente si el usuario esta registrado

#Para el decorador, los permisos se deben especificar de la siguiente forma: <app_label>.<permiso>_<modelo>
#Teniendo que estar el nombre del modelo en minusculas

@permission_required('rango.change_page', login_url='/rango/login/')
def edit_page(request, category_name_slug, page_name_slug):


#	user = request.user
#	if not user.has_perm('rango.change_page'):

#		return HttpResponse("El usuario no tiene los permisos necesarios")

	instance = get_object_or_404(Page, slug = page_name_slug)

	if request.method == 'POST':

		form = PageForm(request.POST or None, instance = instance)

		if form.is_valid():

			form.save()

			#Probably better to use a redirect here
			return category(request, category_name_slug)

		else:
			print form.errors

	else:
		form = PageForm()


	context_dict = {'form': form, 'category_name_slug': category_name_slug, 'page_name_slug': page_name_slug}

	return render(request, 'rango/edit_page.html', context_dict)


@permission_required('rango.delete_page', login_url='/rango/login/')
def delete_page(request, category_name_slug, page_name_slug):


	page = get_object_or_404(Page, slug = page_name_slug)
	page.delete()

	return HttpResponseRedirect(reverse('category', args = (category_name_slug,)))


# ------------------------------------------------------------------------- #

def register(request):

	# Booleano que indica a la plantilla si el registro ha sido correcto o no
	registered = False

	# Si es un HTTP POST, estamos interesados en procesar la informacion del formulario
	if request.method == 'POST':

		# Intentamos recopilar infromacion del formulario
		# Usamos los dos formularios para usuarios
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid
		if user_form.is_valid() and profile_form.is_valid():

			# Guardamos la informacion del formulario en la BBDD
			user = user_form.save(commit = False)

			# Encriptamos la contrasenha con el metodo set_password
			# Una vez encriptada, actualizamos el objeto user
			user.set_password(user.password)

			#user.user_permissions(rango.)
			#user.has_perm(rango.add_Page)
			#user.has_perm(rango.change_Page)


			user.save()

			# Anhadimos el commit = False para posponer el gardado del modelo
			profile = profile_form.save(commit = False)
			profile.user = user

			# Guardamos la instancia
			profile.save()

			# Indicamos que no ha habido problemas a la hora de resgistrar el nuevo usuario
			registered = True


		# Formulario invalido - Fallos o algo mas?
		# Imprimimos los errores en la terminal
		else:
			print user_form.errors, profile_form.errors

	# Not HTTP POST, por tanto renderizamos nuestro formulario usando dos instancias de ModelForm
	# Estos formularios estaran vacios, preparados para la entrada por parte del usuario
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Renderiza la plantilla dependiendo del contexto
	return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# ------------------------------------------------------------------------- #

def user_login(request):

	if request.method == 'POST':

		# Gather the username and password provided by the user
		# This infromation is obtained from the login form
		#		We use request.POST.get('<variable>') as oposed to request.POST['<variable>'],
		#		because the request.POST.get('<variable>') returns None, if the value does not exists,
		# 		while teh request.POST['<variable>'] will raise key error exception

		username = request.POST.get('username')
		password = request.POST.get('password')

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found
		if user:

			# Is the account active? It could have been disabled
			if user.is_active:

				# If the account is valid and active, we can log the user in
				# We'll send the user back to the homepage
				login(request, user)
				return HttpResponseRedirect('/rango/')

			else:

				# An inactive account was used - no loggin in!
				return HttpResponse("Your Django account is disabled")

		else:

			# Bad login details were provided. So we can't log the user in
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied")

	# The request is not a HTTP POST, so display hte login form
	# This scenario would most likely be a HTTP  GET
	else:

		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):


	logout(request)

	return HttpResponseRedirect('/rango/')

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







