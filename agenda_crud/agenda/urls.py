from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import register, custom_login, buscar_contactos, contact_detail

# URLs para contactos
contact_urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='contact_create'),
    path('<int:pk>/edit/', views.contact_update, name='contact_update'),
    path('<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('<int:pk>/', contact_detail, name='contact_detail'),
]

# URLs para autenticación
auth_urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),  # O usa auth_views.LoginView
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/cerrar_sesion.html'), name='logout'),
]

urlpatterns = [
    path('contacts/', include(contact_urlpatterns)),
    path('accounts/', include(auth_urlpatterns)),
    path('buscar-contactos/', buscar_contactos, name='buscar_contactos'),
]