from .models import Producto
from .serializers import ProductoSerializer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from .forms import productoForm

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class= ProductoSerializer
    renderer_classes = [JSONRenderer]

def agregar_producto(req):
    form = productoForm
    return render(req, 'agregar.html', {'form': form})

def prueba_view(req):
    return render(req, 'prueba.html')