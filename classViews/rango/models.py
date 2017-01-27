from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Clase que representa las diferentes categorias a las que puede pertenecer una pagina
class Category(models.Model):

	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):

		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):

		return self.name

# Clase que representa a las diferentes paginas de la web
class Page(models.Model):

	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):

		self.slug = slugify(self.title)
		super(Page, self).save(*args, **kwargs)

	def __str__(self):

		return self.title


# Clase asociada con la clase User, que la extiende

class UserProfile(models.Model):

	# This line is required. Links UserProfile to a User model instance
	user = models.OneToOneField(User)

	# The additional atributes we wish to include
	website = models.URLField(blank = True)

	# Override the __str__() methos to return out something meaningfull
	def __str__(self):

		return self.user.username











