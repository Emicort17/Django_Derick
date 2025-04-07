from django.db import models
from categorias.models import Categoria

# Create your models here.
class Producto (models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField()
    categoria = models.ForeignKey(Categoria, 
                                  on_delete = models.SET_NULL,
                                  null= True,
                                  blank= True)
    
    def __str__(self):
        return self.nombre 
