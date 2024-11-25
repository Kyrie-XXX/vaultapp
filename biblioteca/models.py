from django.db import models

class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    fecha_publicacion = models.DateField(null=True, blank=True)
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
