from django.urls import path
from . import views
from .views import register  # Importa la vista de registro
from django.contrib.auth import views as auth_views
from .views import custom_login
from .views import buscar_contactos



urlpatterns = [
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/edit/', views.contact_update, name='contact_update'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('accounts/register/', register, name='register'),  # URL de registro
    #path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/login/', custom_login, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/cerrar_sesion.html'), name='logout'),
    path('buscar-contactos/', buscar_contactos, name='buscar_contactos'),

]