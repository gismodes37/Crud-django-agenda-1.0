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
from django.db.models import Q  # Para búsquedas avanzadas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Para paginación
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


def es_administrador(user):
    """Verifica si el usuario es administrador."""
    return user.is_authenticated and user.is_staff

@user_passes_test(es_administrador, login_url='/accounts/login/')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Usuario {user.username} creado exitosamente!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})



# Lista de contactos
@login_required
def contact_list(request):
#    contacts = Contact.objects.filter(usuario=request.user)  # Muestra los contactos por usuario
    query = request.GET.get('q')  # Obtén el término de búsqueda
    contacts = Contact.objects.all()

    if query:
        # Filtra los contactos que coincidan con el término de búsqueda
        contacts = contacts.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query) |
            Q(razon_social__icontains=query)
        )

     # Paginación: Muestra 10 contactos por página
    paginator = Paginator(contacts, 10)
    page = request.GET.get('page')  # Obtén el número de página

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        contacts = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, muestra la última página
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'agenda/contact_list.html', {'contacts': contacts, 'query': query})


# Buscar contactos
from django.http import JsonResponse
from django.template.loader import render_to_string

def buscar_contactos(request):
    query = request.GET.get('q', '').strip()  # Elimina espacios en blanco

    # Validación básica
    if len(query) < 2:  # Requiere al menos 2 caracteres
        return JsonResponse({'html': '<p>Ingresa al menos 2 caracteres para buscar.</p>'})

    contacts = Contact.objects.all()

    if query:
        contacts = contacts.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query) |
            Q(razon_social__icontains=query)
        )

    html = render_to_string('agenda/partials/contactos_tabla.html', {'contacts': contacts})
    return JsonResponse({'html': html})



# Crear contacto
@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.creado_por = request.user  # Asigna el usuario actual
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
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.modificado_por = request.user  # Asigna el usuario actual
            contact.save()
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