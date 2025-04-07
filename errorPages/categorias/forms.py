from django import forms
from .models import Categoria

#Podemos crear un formulario para cada modelo que exista

class categoriaForm(forms.ModelForm):
#clase meta (Metainfo del formulario)
    class Meta:
        #Definir de que modelo se basa el formulario
        model = Categoria
        
        #Definir que campos van a ser incluidos en el formulario
        fields = ['nombre', 'imagen']
        
        #Definir como se deben de ver o que atributos tienen los campos
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la categoria'
                }
            ),
                        
            'imagen': forms.URLInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'URL de la imagen de la categoria'
                }
            )
        }
        
        #Etiquetas o labels persnoalizados
        
        labels= {
            'nombre': 'Nombre del producto',
            'imagen': 'URL de la imagen'
        }
        
        #Mensaje de errir personalizados
        
        error_messages = {
            'nombre': {'required': 'EL nombre es obligatio'},
            'imagen': {'required': 'La imagen no puede estar vacia'},
        }