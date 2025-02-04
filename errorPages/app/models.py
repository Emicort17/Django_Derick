from django.db import models

class ErrorLog (models.Model):
    #es igual a ponder un varchar(10)
    codigo = models.CharField(max_length=10)
    #Longtext
    mensaje = models.TextField()
    #es igual a Date(now())
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{codigo} - {mensaje}"