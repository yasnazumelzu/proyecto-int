from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import Usuario

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su usuario"
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su contraseña"
        })
    )

class UsuarioForm(forms.ModelForm):
    """Formulario para crear un nuevo usuario"""
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text="Mínimo 8 caracteres"
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UsuarioEditForm(forms.ModelForm):
    """Formulario para editar un usuario existente"""
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GrupoForm(forms.ModelForm):
    """Formulario para crear/editar grupos"""
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10'}),
        }
