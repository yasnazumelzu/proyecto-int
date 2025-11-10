from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render

def inicio(request):
    return render(request, 'usuarios/inicio.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Mensaje de bienvenida según el usuario
            if user.username == 'matrona':
                messages.success(request, f"Bienvenida Matrona {user.username.capitalize()} 👩‍⚕️")
                return redirect('dashboard_matrona')
            elif user.username == 'medico':
                messages.success(request, f"Bienvenido Dr. {user.username.capitalize()} 🩺")
                return redirect('dashboard_medico')
            elif user.username == 'enfermero':
                messages.success(request, f"Bienvenido Enfermero {user.username.capitalize()} 💉")
                return redirect('dashboard_enfermero')
            elif user.username == 'administrativo':
                messages.success(request, f"Bienvenido {user.username.capitalize()} 🗂️")
                return redirect('dashboard_administrativo')
            else:
                messages.success(request, f"Bienvenido/a {user.username}")
                return redirect('login')
        else:
            messages.error(request, "❌ Usuario o contraseña incorrectos. Intente nuevamente.")
            return redirect('login')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')

