from django.db import models


# class Endereco(models.Model):
#     bairro=models.CharField(max_length=100)
#     rua=models.CharField(max_length=100)
#     cidade=models.CharField(max_length=100)
#     numero=models.CharField(max_length=100)
#     cep=models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.cidade



# Usuário base (pode ser cuidador ou família)
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15)
    senha = models.CharField(max_length=128)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_nasc = models.DateField()

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    nome = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nome


# Modelo específico para Cuidadores
class Cuidador(Usuario):
    formacao = models.CharField(max_length=200, null=True, blank=True)
    especialidade = models.CharField(max_length=200, null=True, blank=True)
    experiencia = models.IntegerField(null=True, blank=True)
    disponibilidade = models.CharField(max_length=200, null=True, blank=True)
    cidades = models.ManyToManyField(Cidade, blank=True, related_name='cuidadores')

    def __str__(self):
        return self.nome




# Modelo específico para Cliente
class Cliente(Usuario):
    necessidade=models.TextField()
    turno_preferencia=models.CharField()

    def __str__(self):
        return self.nome


class Solicitacao(models.Model):
    data_solicitacao=models.DateField()
    turno=models.CharField(max_length=100)
    horario_inicial=models.TimeField()
    horario_final=models.TimeField()
    status=models.CharField(max_length=100)
    observacao=models.TextField()
    descricao=models.TextField()
    cliente=models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cuidador=models.ForeignKey(Cuidador, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.descricao

# Exemplo : avaliação entre cliente e cuidador
class Avaliacao_Cliente(models.Model):
    nota=models.FloatField()
    comentario=models.TextField()
    data_avalicao=models.DateTimeField(auto_now_add=True)
    cliente=models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    solicitacao=models.ForeignKey(Solicitacao, on_delete=models.DO_NOTHING)
    cuidador_avaliado=models.ForeignKey(Cuidador, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.comentario

class Avaliacao_Cuidador(models.Model):
    nota=models.FloatField()
    comentario=models.TextField()
    data_avalicao=models.DateTimeField(auto_now_add=True)
    cliente_avaliado = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.DO_NOTHING)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.comentario


class Mensagem(models.Model):
    conteudo=models.CharField(max_length=100)
    data_msg=models.DateTimeField(auto_now_add=True)
    solicitacao=models.ForeignKey(Solicitacao, on_delete=models.DO_NOTHING)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.conteudo




