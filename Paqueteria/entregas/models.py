from django.db import models

# Create your models here

# Un destinatario es una persona a la que se debe entregar un paquete
class Destinatario(models.Model):

	direccion = models.CharField(max_length=100)
	ciudad = models.CharField(max_length=100)
	distancia = models.IntegerField()
	
	def __str__(self):

		return self.direccion


class Ruta(models.Model):

	nombre = models.CharField(max_length=100)

	def __str__(self):

		return self.nombre


class Paquete(models.Model):

	contenido = models.CharField(max_length=100)
	valor = models.IntegerField()

	destinatario = models.ForeignKey(Destinatario)
	ruta = models.ForeignKey(Ruta)

	def __str__(self):

		return self.contenido

