from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'id': 'password_1',
            'class': 'form-control w-25',
            'placeholder': 'Ingrese su contraseña',
        }),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'id': 'password_2',
            'class': 'form-control w-25',
            'placeholder': 'Confirme su contraseña',
        }),
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'id': 'email',
                    'class': 'form-control w-25',
                    'placeholder': 'Correo electrónico',
                    'pattern': '^[0-9]{5}tn[0-9]{3}@utez\.edu\.mx$'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control w-25',
                    'placeholder': 'Ingrese su nombre completo',
                    'maxlength': '100',
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'class': 'form-control w-25',
                    'placeholder': 'Ingrese su apellido completo',
                    'maxlength': '100',
                }
            ),
            'control_number': forms.TextInput(
                attrs={
                    'class': 'form-control w-25',
                    'placeholder': 'Ingrese su matrícula',
                    'pattern': '^[0-9]{5}tn[0-9]{3}$',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control w-25',
                    'placeholder': 'Ingrese su edad',
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'id': 'tel',
                    'class': 'form-control w-25',
                    'placeholder': 'Ingrese su número de teléfono (10 dígitos)',
                    'pattern': '^[0-9]{10}$',
                    'maxlength': '10',
                }
            )
        }

    def clean_control_number(self):
        control_number = self.cleaned_data.get('control_number')
        if not re.match(r'^[0-9]{5}tn[0-9]{3}$', control_number):
            raise forms.ValidationError("La matrícula no tiene el formato correcto.")
        return control_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[0-9]{5}tn[0-9]{3}@utez\.edu\.mx$', email):
            raise forms.ValidationError("El correo electrónico no tiene el formato correcto.")
        return email

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if not re.match(r'^[0-9]{10}$', tel):
            raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos.")
        return tel

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 1 or len(name) > 100:
            raise forms.ValidationError("El nombre debe tener entre 1 y 100 caracteres.")
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if len(surname) > 100:
            raise forms.ValidationError("El apellido no puede tener más de 100 caracteres.")
        return surname

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control w-25',
            'placeholder': 'Ingrese su correo electrónico',
        }),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control w-25',
            'placeholder': 'Ingrese su contraseña',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if email and not email.endswith('@utez.edu.mx'):
            raise ValidationError("El correo electrónico debe ser del dominio @utez.edu.mx.")

        if password:
            if len(password) < 8:
                raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if not re.search(r'[!#$%&?]', password):
                raise ValidationError("La contraseña debe contener al menos un símbolo (!, #, $, %, & o ?).")
            if not re.search(r'\d', password):
                raise ValidationError("La contraseña debe contener al menos un número.")

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise ValidationError("Usuario o contraseña incorrectos.")

        return cleaned_data