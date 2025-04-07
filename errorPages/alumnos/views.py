from .models import Alumno
from .serializers import AlumnoSerializer
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from .forms import AlumnoForm
from django.shortcuts import render


# Create your views here.
class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    renderer_classes = [JSONRenderer]
    #Método para limitar los http 
    #http_method_names= ["GET", "POST"]

def agregar_alumnos(req):
    form = AlumnoForm
    return render(req, 'alumnoInterface.html', {'form': form})