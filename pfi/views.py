

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from pfi.models import *
from pfi.forms import *
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.core import serializers
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Solicitacao
from django.views.generic import DetailView
from django.db.models import Avg
from .models import Cuidador, Avaliacao_Cliente


# Create your views here.
cuidador_logado: Cuidador = None


class IndexTemplateView(TemplateView):
    template_name = 'index.html'


class CuidadoresTemplateView(ListView):
    template_name = 'cuidadores.html'
    model = Cuidador
    context_object_name = 'cuidadores'

    def get_queryset(self):
        return (
            Cuidador.objects
            .annotate(media_avaliacao=Avg("avaliacao_cliente__nota"))
            .distinct()
            .order_by("-media_avaliacao")[:4]
        )





class SobreTemplateView(TemplateView):
    template_name = 'sobre.html'




def login(request):
    msg_erro = None
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        tipo = request.POST.get('tipo_usuario')  # <-- só isso

        user = Usuario.objects.filter(email=email, senha=senha).first()

        if user:
            # verifica se é cuidador no banco
            is_cuidador = Cuidador.objects.filter(pk=user.pk).exists()

            # --- valida o tipo escolhido ---
            if tipo == "cuidador" and not is_cuidador:
                return render(request, 'login.html', {"msg_erro": "Este e-mail não é de cuidador."})

            if tipo == "cliente" and is_cuidador:
                return render(request, 'login.html', {"msg_erro": "Este e-mail não é de cliente."})

            if tipo == "cuidador":
                cuidador = Cuidador.objects.get(pk=user.pk)
                request.session["cuidador_id"] = cuidador.id

            # login normal
            request.session["user_id"] = user.id
            request.session["is_cuidador"] = is_cuidador

            usuario_serializado = serializers.serialize('json', [user])
            request.session["user_logado"] = usuario_serializado

            return redirect('home')

        else:
            msg_erro = "Email ou senha incorretos."

    return render(request, 'login.html', {'msg_erro': msg_erro})

def logout_view(request):
    request.session.flush()
    return redirect('login')


from .models import Cuidador, Cliente, Cidade


def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        cpf = request.POST.get("cpf")
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
                cpf=cpf,
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
                cpf=cpf,
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
        query = self.request.GET.get('cidade', '')  # pega o valor do input
        qs = Cuidador.objects.all()
        if query:
            qs = qs.filter(cidades__nome__icontains=query)
        # Anotar a média das avaliações
        qs = qs.annotate(nota_media=Avg('avaliacao_cliente__nota'))
        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('cidade', '')  # mantém o valor no input
        return context



class CuidadorDetailView(DetailView):
    model = Cuidador
    template_name = "perfil_cuidador.html"
    context_object_name = "cuidador"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cuidador = self.get_object()

        # Calcula a média das avaliações (pode ter decimal)
        media = Avaliacao_Cliente.objects.filter(cuidador_avaliado=cuidador).aggregate(
            media=Avg('nota')
        )['media']

        context['nota_media'] = media if media else 0
        return context

class EditarPerfilClienteView(UpdateView):
    model = Cliente
    template_name = "editar_perfil_cliente.html"  # você pode criar o HTML baseado no do cuidador
    fields = ["nome", "email", "telefone", "foto", "necessidade", "turno_preferencia"]
    success_url = reverse_lazy("editar_perfil_cliente")

    def get_object(self, queryset=None):
        user_id = self.request.session.get("user_id")
        if not user_id:
            messages.error(self.request, "Você precisa estar logado para editar o perfil.")
            return redirect("login")
        return Cliente.objects.get(pk=user_id)

    def form_valid(self, form):
        cliente = form.save(commit=False)

        # Salvar foto se houver
        if self.request.FILES.get("foto"):
            cliente.foto = self.request.FILES["foto"]

        cliente.save()

        # Atualiza sessão
        usuario_serializado = serializers.serialize('json', [cliente])
        self.request.session['user_logado'] = usuario_serializado
        self.request.session['user_id'] = cliente.id

        messages.success(self.request, "Perfil atualizado com sucesso!")
        return super().form_valid(form)


class SolicitacoesCuidadorView(ListView):
    model = Solicitacao
    template_name = "solicitacoes_cuidador.html"
    context_object_name = "solicitacoes"


def CriarSolicitacoes(request, pk):
    cuidador = Cuidador.objects.get(pk=pk)
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")
        cliente = Cliente.objects.get(pk=user_id)
        data_solicitacao = request.POST.get("data_solicitacao")
        turno = request.POST.get("turno")
        horario_inicial = request.POST.get('horario_inicial')
        horario_final = request.POST.get('horario_final')
        descricao = request.POST.get('descricao')
        observacao = request.POST.get('observacao')
        solicitacao = Solicitacao(
            cuidador=cuidador,
            cliente=cliente,
            data_solicitacao=data_solicitacao,
            turno=turno,
            horario_inicial=horario_inicial,
            horario_final=horario_final,
            descricao=descricao,
            observacao=observacao,
            status="pendente"
        )
        solicitacao.save()
        return redirect('home')
    return render(request, 'solicitar_cuidador.html', {'cuidador': cuidador})


def solicitar_cuidador(request, cuidador_id):
    return render(request, "solicitar_cuidador.html")


# ============================================================
#  CLIENTE - MINHAS SOLICITAÇÕES
# ============================================================

def minhas_solicitacoes_cliente(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    cliente = Cliente.objects.filter(usuario_ptr_id=user_id).first()

    # Pegar todas as solicitações do cliente e anotar a média das avaliações
    solicitacoes = (
        Solicitacao.objects.filter(cliente=cliente)
        .annotate(media_avaliacao=Avg('avaliacao_cliente__nota'))
        .order_by("-id")
    )

    return render(request, "minhas_solicitacoes.html", {"solicitacoes": solicitacoes})


# LISTAR PENDENTES
def solicitacoes_pendentes(request):
    cuidador = Cuidador.objects.get(usuario_ptr_id=request.session["user_id"])
    solicitacoes = Solicitacao.objects.filter(cuidador=cuidador, status="pendente")
    return render(request, "solicitacoes_pendentes.html", {"solicitacoes": solicitacoes})



# LISTAR ACEITAS
def solicitacoes_aceitas(request):
    cuidador = Cuidador.objects.get(usuario_ptr_id=request.session["user_id"])
    solicitacoes = Solicitacao.objects.filter(cuidador=cuidador, status="aceita")
    return render(request, "solicitacoes_aceitas.html", {"solicitacoes": solicitacoes})


# LISTAR RECUSADAS/CANCELADAS
def solicitacoes_recusadas(request):
    cuidador = Cuidador.objects.get(usuario_ptr_id=request.session["user_id"])
    solicitacoes = Solicitacao.objects.filter(
        cuidador=cuidador,
        status__in=["recusada", "cancelada"]
    )
    return render(request, "solicitacoes_recusadas.html", {"solicitacoes": solicitacoes})


# ACEITAR
def aceitar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)
    solicitacao.status = "aceita"
    solicitacao.save()
    return redirect("solicitacoes_pendentes")


# RECUSAR
def recusar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)
    solicitacao.status = "recusada"
    solicitacao.save()
    return redirect("solicitacoes_pendentes")


# CANCELAR (somente quando já está aceita)
def cancelar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)
    solicitacao.status = "cancelada"
    solicitacao.save()
    return redirect("solicitacoes_recusadas")

def cancelar_solicitacao_cliente(request, id):
    solicitacao = Solicitacao.objects.get(id=id)
    solicitacao.status = "cancelada"
    solicitacao.save()
    return redirect("minhas_solicitacoes")


# CONCLUIR
def concluir_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)
    solicitacao.status = "concluida"
    solicitacao.save()
    return redirect("solicitacoes_aceitas")


# EXCLUIR DEFINITIVAMENTE
def excluir_solicitacao(request, id):
    try:
        solicitacao = Solicitacao.objects.get(id=id)
        # Só permite apagar se não for pendente
        if solicitacao.status != "pendente":
            # Apaga registros dependentes
            Avaliacao_Cliente.objects.filter(solicitacao=solicitacao).delete()
            Avaliacao_Cuidador.objects.filter(solicitacao=solicitacao).delete()
            Mensagem.objects.filter(solicitacao=solicitacao).delete()

            # Agora apaga a própria solicitação
            solicitacao.delete()
    except Solicitacao.DoesNotExist:
        pass  # se não existir, ignora

    # Mantém o usuário na tela correta
    return redirect(request.META.get('HTTP_REFERER', 'minhas_solicitacoes'))




def aceitar_solicitacao(request, id):
    solicitacao = get_object_or_404(Solicitacao, id=id)
    solicitacao.status = 'aceita'
    solicitacao.save()
    return redirect('solicitacoes_cuidador')  # volta pra mesma tela


def recusar_solicitacao(request, id):
    solicitacao = get_object_or_404(Solicitacao, id=id)
    solicitacao.status = 'recusada'
    solicitacao.save()
    return redirect('solicitacoes_cuidador')  # volta pra mesma tela


def EditarPerfilCuidadorView(request):
    iduser = request.session["user_id"]
    print('iduser:', iduser)
    cuidador = Cuidador.objects.filter(usuario_ptr_id=iduser).first()
    print('cuidador:', cuidador)
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        foto = request.POST.get("foto")
        especialidade = request.POST.get("especialidade")
        disponibilidade = request.POST.get("disponibilidade")

        print(nome)
        print(email)
        print(telefone)
        print(foto)
        print(especialidade)
        print(disponibilidade)

        cuidador.nome = nome
        cuidador.email = email
        cuidador.telefone = telefone
        cuidador.foto = foto
        cuidador.especialidade = especialidade
        cuidador.disponibilidade = disponibilidade

        cuidador.save()
        return redirect("home")

    else:
        dados = {'cuidador': cuidador}
        return render(request, "editar_perfil.html", context=dados)


def avaliar_cuidador(request, solicitacao_id):
    # pegar cliente logado
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    cliente = Cliente.objects.filter(pk=user_id).first()
    solicitacao = Solicitacao.objects.filter(pk=solicitacao_id).first()

    if not cliente or not solicitacao:
        return redirect("minhas_solicitacoes")

    if request.method == "POST":
        nota = float(request.POST.get("nota", 0))
        if 0 < nota <= 5:
            Avaliacao_Cliente.objects.create(
                nota=nota,
                cliente=cliente,
                solicitacao=solicitacao,
                cuidador_avaliado=solicitacao.cuidador
            )
            messages.success(request, f"Você avaliou {solicitacao.cuidador.nome} com {nota} estrelas!")
        else:
            messages.error(request, "Nota inválida. Escolha de 1 a 5.")

        return redirect("minhas_solicitacoes")

    # Se for GET, renderiza o template de avaliação
    return render(request, "avaliacao_cuidador.html", {"solicitacao": solicitacao})
