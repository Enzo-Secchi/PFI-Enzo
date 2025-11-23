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
from django.conf import settings
from django.conf.urls.static import static
from pfi.views import logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('home/', IndexTemplateView.as_view(), name='home'),
    path('usuario', UsuarioListView.as_view(), name='usuario'),
    path('cuidadores/', CuidadoresTemplateView.as_view(), name='cuidadores'),
    path('sobre/', SobreTemplateView.as_view(), name='sobre'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path("localizacao/", LocalizacaoView.as_view(), name="localizacao"),
    path("cuidador/<int:id>/", CuidadorDetailView.as_view(), name="ver_perfil"),
    path("editar-perfil/cuidador/", EditarPerfilCuidadorView, name="editar_perfil_cuidador"),
    path("editar-perfil/cliente/", EditarPerfilClienteView.as_view(), name="editar_perfil_cliente"),
    path("cuidador/solicitacoes/", SolicitacoesCuidadorView.as_view(), name="solicitacoes_cuidador"),
    path("solicitar-cuidador/<int:pk>/", CriarSolicitacoes, name="cadastrar_solicitacao"),
    path('minhas-solicitacoes/cliente/', minhas_solicitacoes_cliente, name='minhas_solicitacoes_cliente'),
    path('minhas-solicitacoes/', views.minhas_solicitacoes_cliente, name='minhas_solicitacoes'),



    path('cuidador/solicitacoes/aceitar/<int:id>/', views.aceitar_solicitacao, name='aceitar_solicitacao'),
    path('cuidador/solicitacoes/recusar/<int:id>/', views.recusar_solicitacao, name='recusar_solicitacao'),


    path("cuidador/solicitacoes/pendentes/", solicitacoes_pendentes, name="solicitacoes_pendentes"),
    path("cuidador/solicitacoes/aceitas/", solicitacoes_aceitas, name="solicitacoes_aceitas"),
    path("cuidador/solicitacoes/recusadas/", solicitacoes_recusadas, name="solicitacoes_recusadas"),

    path("cuidador/solicitacao/<int:id>/aceitar/", aceitar_solicitacao, name="aceitar_solicitacao"),
    path("cuidador/solicitacao/<int:id>/recusar/", recusar_solicitacao, name="recusar_solicitacao"),
    path('solicitacoes/cancelar/<int:id>/', cancelar_solicitacao_cliente, name='cancelar_solicitacao_cliente'),

    path("cuidador/solicitacao/<int:id>/concluir/", concluir_solicitacao, name="concluir_solicitacao"),
    path("cuidador/solicitacao/<int:id>/cancelar/", cancelar_solicitacao, name="cancelar_solicitacao"),
    path("cuidador/solicitacao/<int:id>/excluir/", excluir_solicitacao, name="excluir_solicitacao"),

    path("avaliar/solicitacao/<int:solicitacao_id>/", avaliar_cuidador, name="avaliar_cuidador"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
