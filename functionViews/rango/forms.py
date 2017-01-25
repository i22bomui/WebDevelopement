from django import forms
from django.contrib.auth.models import User
from .models import Page, Category, UserProfile

#Form representing the different Categories

class CategoryForm(forms.ModelForm):

	#name = forms.CharField(max_length=128, help_text="Please enter the category name")
	#views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	#likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	#slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	#An inline class to provide additional information on the form
	class Meta:

		#Provide an association between the ModelForm and a model
		model = Category

		# Los campos que saldran a rellenar seran los especificados dentro de 'fields' - Seran visibles
		fields = ('name',)


#Form representing the different Pages

class PageForm(forms.ModelForm):

	#title = forms.CharField(max_length=128, help_text="Please enter the title of the page")
	#url = forms.URLField(max_length=200, help_text="Please enter the URL of the page")
	#views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	#slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:

		model = Page

		#No anadimos el campo de la clave foranea al modelo que usaremos para la form
		exclude = ('category',)
		fields = ('title', 'url',)


	def clean(self):

		# Cleaned_data es un diccioneario proporcionado por ModelForm
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		#If url is not empty and doesn't start with 'http://', prepend 'http://'
		if url and not url.startswith('http://'):

			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data


# -------------------------------------------------------------------------------------- #


class UserForm(forms.ModelForm):

	# Esta redefinicion hace que se oculte la contrasenha del usuario en el formulario
	password = forms.CharField(widget = forms.PasswordInput)
	permissions = forms.BooleanField()

	class Meta:

		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

	class Meta:

		model = UserProfile
		fields = ('website',)












