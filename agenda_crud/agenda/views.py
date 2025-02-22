from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Contact
from .forms import UserRegisterForm, ContactForm  # Importaciones desde forms.py
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.urls import path

class CustomLogoutView(LogoutView):
    template_name = './registration/cerrar_sesion.html'  # Especifica la nueva plantilla
    
    
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Vista de inicio de sesion perzonalizada
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Hola, {user.username}! Bienvenido de nuevo.')
            return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'registration/login.html')



def home(request):
    # Obtener el nombre del usuario autenticado
    user_name = request.user.username if request.user.is_authenticated else "Invitado"
    return render(request, 'agenda/home.html', {'user_name': user_name})

# Registro de usuarios
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario en la base de datos
            login(request, user)  # Inicia sesión automáticamente después del registro
            messages.success(request, f'¡Bienvenido, {user.username}!')  # Mensaje personalizado
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})



# Lista de contactos
@login_required
def contact_list(request):
#    contacts = Contact.objects.filter(usuario=request.user)  # Muestra los contactos por usuario
    contacts = Contact.objects.all()  # Muestra todos los contactos
    return render(request, 'agenda/contact_list.html', {'contacts': contacts})

# Crear contacto
@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.usuario = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'agenda/contact_form.html', {'form': form})

# Editar contacto
@login_required
def contact_update(request, pk):
#    contact = get_object_or_404(Contact, pk=pk, usuario=request.user)
    contact = get_object_or_404(Contact, pk=pk)  # No se verifica el usuario
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'agenda/contact_form.html', {'form': form})


# Eliminar contacto
@login_required
def contact_delete(request, pk):
#    contact = get_object_or_404(Contact, pk=pk, usuario=request.user)
    contact = get_object_or_404(Contact, pk=pk)  # No se verifica el usuario
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'agenda/contact_confirm_delete.html', {'contact': contact})