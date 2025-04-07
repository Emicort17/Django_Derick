from django.db import models

# Create your models here.
class Alumno(models.Model):
        name = models.CharField(max_length=100)
        surname = models.CharField(max_length=100)
        age = models.IntegerField()
        matricula = models.CharField(unique= True, max_length=15)
        email = models.EmailField(unique= True, max_length=100)
    
        def __str__(self):
            return self.name 