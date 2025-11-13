"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from pfi.views import *
from django.urls import path
from pfi import views
from pfi.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexTemplateView.as_view(), name='home'),
    path('usuario', UsuarioListView.as_view(), name='usuario'),
    path('cuidadores/', CuidadoresTemplateView.as_view(), name='cuidadores'),
    path('sobre/', SobreTemplateView.as_view(), name='sobre'),
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path("localizacao/", LocalizacaoView.as_view(), name="localizacao"),
    path("cuidador/<int:id>/", CuidadorDetailView.as_view(), name="ver_perfil"),
    path("editar-perfil/", EditarPerfil, name="editar_perfil"),
]
