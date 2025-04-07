from django.urls import path
from .views import *

urlpatterns= [
    path('ver/', ver_categoria, name='ver'),
    path('registrar/', agregar_categoria, name='agregar'),
    path('api/get/', lista_categorias, name='lista'),
    path('json/', json_view, name="json"),
    path('api/post/', registrar_categoria, name='post')
]