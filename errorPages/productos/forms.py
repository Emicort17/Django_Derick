from django import forms
from .models import Producto

#Podemos crear un formulario para cada modelo que exista

class productoForm(forms.ModelForm):
#clase meta (Metainfo del formulario)
    class Meta:
        #Definir de que modelo se basa el formulario
        model = Producto
        
        #Definir que campos van a ser incluidos en el formulario
        fields = ['nombre', 'precio', 'imagen', 'categoria']
        
        #Definir como se deben de ver o que atributos tienen los campos
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del producto'
                }
            ),
            
            'precio': forms.NumberInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Pon un precio al producto'
                }
            ),
                        
            'imagen': forms.URLInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'URL de la imagen del producto'
                }
            ),
            
            'categoria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }
        
        #Etiquetas o labels persnoalizados
        
        labels= {
            'nombre': 'Nombre del producto',
            'precio': 'Precio en MXN',
            'imagen': 'URL de la imagen',
            'categoria': 'Categoria del producto'
        }
        
        #Mensaje de errir personalizados
        
        error_messages = {
            'nombre': {'required': 'EL nombre es obligatio'},
            'precio': {'required': 'EL precio no puede estar vacio', 'invalid': 'Ingrese un número valido'},
        }