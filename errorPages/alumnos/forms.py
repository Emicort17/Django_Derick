from django import forms
from .models import Alumno

# Creamos un formulario basado en el modelo Alumno
class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        
        # Definimos qué campos van a ser incluidos en el formulario
        fields = ['name', 'surname', 'age', 'matricula', 'email']
        
        # Definimos los widgets para cada campo
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del alumno',
                    'id': 'name'
                }
            ),
            
            'surname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellido del alumno',
                    'id': 'surname'
                }
            ),
            
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Edad del alumno',
                    'id': 'age'
                }
            ),
            
            'matricula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Matrícula del alumno',
                    'id': 'matricula'
                }
            ),
            
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo del alumno',
                    'id': 'email'
                }
            ),
        }
        
        # Definimos etiquetas personalizadas para los campos
        labels = {
            'name': 'Nombre del alumno',
            'surname': 'Apellidos del alumno',
            'age': 'Edad del alumno',
            'matricula': 'Matrícula del alumno',
            'email': 'Correo del alumno',
        }
        
        # Mensajes de error personalizados para cada campo
        error_messages = {
            'name': {'required': 'El nombre es obligatorio'},
            'surname': {'required': 'Los apellidos no pueden estar vacíos', 'invalid': 'Ingrese un apellido válido'},
            'age': {'required': 'La edad es obligatoria', 'invalid': 'Ingrese un número válido'},
            'matricula': {'required': 'La matrícula es obligatoria'},
            'email': {'required': 'El correo es obligatorio', 'invalid': 'Ingrese un correo válido'},
        }
