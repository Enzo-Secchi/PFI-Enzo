from django.contrib import admin

from pfi.models import *

# Register your models here.
# @admin.register(Endereco)
# class EnderecoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'bairro', 'rua', 'cidade', 'numero', 'cep')
#     ordering = ('-id',)
#     search_fields = ('bairro', 'rua', 'cidade', 'cep')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'cpf', 'telefone', 'data_nasc',)
    ordering = ('-id',)
    search_fields = ('nome', 'email', 'cpf')

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)


@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    fields = ('nome', 'email', 'cpf', 'telefone', 'data_nasc',
              'formacao', 'especialidade', 'experiencia', 'disponibilidade', 'cidades')
    list_display = ('id', 'nome', 'get_cidades', 'formacao', 'especialidade', 'experiencia', 'disponibilidade')
    ordering = ('-id',)
    search_fields = ('nome', 'especialidade', 'formacao')

    def get_cidades(self, obj):
        return ", ".join([c.nome for c in obj.cidades.all()])
    get_cidades.short_description = 'Cidades'



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'necessidade', 'turno_preferencia')
    ordering = ('-id',)
    search_fields = ('nome', 'necessidade')


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'data_solicitacao', 'turno', 'horario_inicial', 'horario_final',
        'status', 'cliente', 'cuidador'
    )
    ordering = ('-id',)
    list_filter = ('status', 'turno')
    search_fields = ('descricao', 'observacao')


@admin.register(Avaliacao_Cliente)
class AvaliacaoClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nota', 'cliente', 'cuidador_avaliado', 'solicitacao', 'data_avalicao')
    ordering = ('-id',)
    search_fields = ('comentario',)


@admin.register(Avaliacao_Cuidador)
class AvaliacaoCuidadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nota', 'cuidador', 'cliente_avaliado', 'solicitacao', 'data_avalicao')
    ordering = ('-id',)
    search_fields = ('comentario',)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'conteudo', 'data_msg', 'solicitacao', 'cuidador')
    ordering = ('-id',)
    search_fields = ('conteudo',)