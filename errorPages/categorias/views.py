import json
from django.shortcuts import render, redirect
from .models import Categoria
from .forms import categoriaForm
from django.http import JsonResponse

# Create your views here.

def agregar_categoria(request):
    #Primero checamos como llegamos a este funcion
    if request.method == 'POST':
        #Llegamos aqui por el envio de un formulario
        form = categoriaForm(request.POST) #Genera un formulario lleno con informacion
        if form.is_valid():
            form.save() #Guarda la informacion en la BD
            return redirect('ver') #Redirige a la vista de productos
    else:
        form = categoriaForm    ()
    return render(request, 'agregarCategoria.html', {'form': form})

#Ver los productos
def ver_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'verCategoria.html', {'categorias': categorias})

#Devuelve el JSON
def lista_categorias(request):
    categorias = Categoria.objects.all()
    #Para enviar un JSON debemos escribir los datos 
    #En un diccionario usando llaves

    #Diccionario personalizado
    data = [
        {
            'nombre' : c.nombre,
            'imagen' : c.imagen
        }
        for c in categorias
    ]

    return JsonResponse(data,safe= False)

def json_view(request):
    return render(request, 'jsoncategoria.html')



def registrar_categoria(req):
    if req.method == 'POST':
        try: 
            data = json.loads(req.body)
            nueva_categoria = Categoria.objects.create(
                nombre = data['nombre'],
                imagen = data['imagen'],
            )
            return JsonResponse({
                'mensaje': 'registro exitoso',
                'id': nueva_categoria.id
                }, status = 201
                 )
        except Exception as e:
            return JsonResponse({
            'error': str(e)
            }, status = 400)
    return JsonResponse({
        'error': 'Método no es POST'
    }, status = 405)