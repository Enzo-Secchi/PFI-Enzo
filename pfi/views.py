from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from pfi.models import *
from pfi.forms import *
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Avg






# Create your views here.

class IndexTemplateView(TemplateView):
    template_name = 'index.html'

class CuidadoresTemplateView(ListView):
    template_name = 'cuidadores.html'
    model = Cuidador
    context_object_name = 'cuidadores'
    # extra_context_name = 'cuidadores' caso precise  add informações extras


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cuidadores = Cuidador.objects.order_by("-avaliacao_cliente")[:4]

        context["cuidadores"] = cuidadores
        return context


class SobreTemplateView(TemplateView):
    template_name = 'sobre.html'

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user =  Usuario()
        # Autenticar usuário
        # Procurar usuário pelo email
        try:
            user = Usuario.objects.get(email=email, senha=senha)
            print(user)
            request.session['user_logado'] = user
        except User.DoesNotExist:
            context = {'msg_erro': 'Usuário não encontrado'}
            return render(request, 'login.html', context=context)


        return redirect('home')
    else:
        return render(request, 'login.html')

# def cadastro(request):
#     if request.method == "POST":
#         nome = request.POST.get("nome")
#         email = request.POST.get("email")
#         telefone = request.POST.get("telefone")
#         senha = request.POST.get("senha")
#         tipo = request.POST.get("tipo")
#
#         print(tipo)
#
#
#         # Campos específicos
#         especialidade = request.POST.get("especialidade")
#         horarios = request.POST.get("horarios")
#         area = request.POST.get("area")
#         necessidades = request.POST.get("necessidades")
#         cidade = request.POST.get("cidade")
#
#         if tipo == 'Cuidador':
#             cuidador = Cuidador()
#             cuidador.nome = nome
#             cuidador.email = email
#             cuidador.telefone = telefone
#             cuidador.senha = senha
#             cuidador.especialidade = especialidade
#             cuidador.horarios = horarios
#             cuidador.area = area
#             cuidador.cidade = cidade
#             cuidador.save()
#
#         return redirect('login')
#
#     return render(request, 'cadastro.html')
from .models import Cuidador, Cliente, Cidade

def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        senha = request.POST.get("senha")
        data_nasc = request.POST.get("data_nasc")
        tipo = request.POST.get("tipo")

        especialidade = request.POST.get("especialidade")
        horarios = request.POST.get("horarios")
        necessidades_texto = request.POST.get("necessidades", "")
        # campo texto com várias cidades separadas por vírgula
        cidades_texto = request.POST.get("cidades", "")

        formacao = request.POST.get("formacao")
        experiencia = request.POST.get("experiencia")

        if tipo == "cuidador":
            cuidador = Cuidador.objects.create(
                nome=nome,
                email=email,
                telefone=telefone,
                senha=senha,
                data_nasc=data_nasc,
                especialidade=especialidade,
                disponibilidade=horarios,
                formacao=formacao,
                experiencia=(int(experiencia) if experiencia else None),
            )
            # processar cidades: criar/get_or_create e adicionar many-to-many
            cidades_list = [c.strip() for c in cidades_texto.split(",") if c.strip()]
            for c_nome in cidades_list:
                cidade_obj, created = Cidade.objects.get_or_create(
                    nome__iexact=c_nome, defaults={"nome": c_nome}
                )
                if not created:
                    cidade_obj = Cidade.objects.filter(nome__iexact=c_nome).first()
                    if not cidade_obj:
                        cidade_obj = Cidade.objects.create(nome=c_nome)
                cuidador.cidades.add(cidade_obj)

        else:
            # organiza necessidades em lista
            lista_necessidades = [n.strip() for n in necessidades_texto.split(",") if n.strip()]
            necessidades_formatado = ", ".join(lista_necessidades)

            turno = request.POST.get("turno")

            Cliente.objects.create(
                nome=nome,
                email=email,
                telefone=telefone,
                senha=senha,
                data_nasc=data_nasc,
                necessidade=necessidades_formatado,  # <-- model usa singular
                turno_preferencia=turno,
            )

        return redirect("login")

    return render(request, "cadastro.html")







class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'formulario.html'
    context_object_name = 'usuario'
    extra_context = {
        'title': 'Usuario Criação',
    }

class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'formulario.html'
    context_object_name = 'usuario'
    extra_context = {'form_titulo': 'Cadastro de Usuario'}

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'excluir_registro.html'
    context_object_name = 'registro'

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuario.html'
    context_object_name = 'usuarios'

class LocalizacaoView(ListView):
    template_name = "localizacao.html"
    model = Cuidador
    context_object_name = 'cuidadores'

    def get_queryset(self):
        cidade_query = self.request.GET.get('cidade')
        qs = super().get_queryset()
        if cidade_query:
            # buscar por nome da cidade (case-insensitive) nas cidades relacionadas
            qs = qs.filter(cidades__nome__icontains=cidade_query).distinct()
        return qs



class CuidadorDetailView(DetailView):
    model = Cuidador
    template_name = "perfil_cuidador.html"
    context_object_name = "cuidador"
    pk_url_kwarg = "id"


def EditarPerfil(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'editar_perfil.html')



class EditarPerfilView(UpdateView):
    model = Cuidador
    template_name = "editar_perfil.html"
    fields = ["nome", "telefone", "especialidade", "cidades"]
    success_url = reverse_lazy("editar_perfil")

    def get_object(self, queryset=None):
        # depois trocar para o usuário logado
        return Cuidador.objects.first()

