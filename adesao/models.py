from django.db import models
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey


LISTA_ESTADOS_PROCESSO = (
    ('0', 'Aguardando preenchimento dos dados cadastrais'),
    ('1', 'Aguardando envio da documentação'),
    ('2', 'Documentação Recebida - Aguarda Análise'),
    ('3', 'Diligência Documental'),
    ('4', 'Encaminhado para assinatura do Secretário SAI'),
    ('5', 'Aguarda Publicação no DOU'),
    ('6', 'Publicado no DOU'),
    ('7', 'Responsável confirmado'),)


# Create your models here.
class Uf(models.Model):
    codigo_ibge = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2)
    nome_uf = models.CharField(max_length=100)

    def __str__(self):
        return self.sigla

    class Meta:
        ordering = ['sigla']


class Cidade(models.Model):
    codigo_ibge = models.IntegerField(unique=True)
    uf = models.ForeignKey('Uf',
        to_field='codigo_ibge',
        on_delete=models.CASCADE)
    nome_municipio = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.nome_municipio

    class Meta:
        ordering = ['nome_municipio']


class Municipio(models.Model):
    localizacao = models.CharField(max_length=50, blank=True)
    numero_processo = models.CharField(max_length=50, blank=True)
    cpf_prefeito = models.CharField(
        max_length=14,
        verbose_name='CPF')
    nome_prefeito = models.CharField(max_length=255)
    cnpj_prefeitura = models.CharField(
        max_length=18,
        verbose_name='CNPJ')
    rg_prefeito = models.CharField(max_length=50, verbose_name='RG')
    orgao_expeditor_rg = models.CharField(max_length=50)
    estado_expeditor = models.ForeignKey('Uf', 
                                         related_name='estado_expeditor',
                                         on_delete=models.CASCADE)
    endereco = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    estado = models.ForeignKey('Uf', on_delete=models.CASCADE)
    cidade = ChainedForeignKey(
        Cidade,
        chained_field='estado',
        chained_model_field='uf',
        show_all=False,
        auto_choose=False,
        blank=True,
        null=True
    )
    telefone_um = models.CharField(max_length=100)
    telefone_dois = models.CharField(max_length=25, blank=True)
    telefone_tres = models.CharField(max_length=25, blank=True)
    endereco_eletronico = models.URLField(max_length=255, blank=True, null=True)
    email_institucional_prefeito = models.EmailField()
    termo_posse_prefeito = models.FileField(
        upload_to='termo_posse',
        max_length=255,
        blank=True,
        null=True)
    rg_copia_prefeito = models.FileField(
        upload_to='rg_copia',
        max_length=255,
        blank=True,
        null=True)
    cpf_copia_prefeito = models.FileField(
        upload_to='cpf_copia',
        max_length=255,
        blank=True,
        null=True)

    def __str__(self):
        return self.cnpj_prefeitura

    class Meta:
        unique_together = ('cidade', 'estado')


class Responsavel(models.Model):
    cpf_responsavel = models.CharField(
        max_length=14,
        verbose_name='CPF')
    rg_responsavel = models.CharField(max_length=25, verbose_name='RG')
    orgao_expeditor_rg = models.CharField(max_length=50)
    estado_expeditor = models.ForeignKey('Uf', on_delete=models.CASCADE)
    nome_responsavel = models.CharField(max_length=100)
    cargo_responsavel = models.CharField(max_length=100)
    instituicao_responsavel = models.CharField(max_length=100)
    telefone_um = models.CharField(max_length=25)
    telefone_dois = models.CharField(max_length=25, blank=True)
    telefone_tres = models.CharField(max_length=25, blank=True)
    email_institucional_responsavel = models.EmailField()

    def __str__(self):
        return self.cpf_responsavel


class Secretario(models.Model):
    cpf_secretario = models.CharField(
        max_length=14,
        verbose_name='CPF')
    rg_secretario = models.CharField(max_length=25, verbose_name='RG')
    orgao_expeditor_rg = models.CharField(max_length=50)
    estado_expeditor = models.ForeignKey('Uf', on_delete=models.CASCADE)
    nome_secretario = models.CharField(max_length=100)
    cargo_secretario = models.CharField(max_length=100)
    instituicao_secretario = models.CharField(max_length=100)
    telefone_um = models.CharField(max_length=25)
    telefone_dois = models.CharField(max_length=25, blank=True)
    telefone_tres = models.CharField(max_length=25, blank=True)
    email_institucional_secretario = models.EmailField()

    def __str__(self):
        return self.cpf_secretario


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_usuario = models.CharField(max_length=100)
    municipio = models.OneToOneField('Municipio', on_delete=models.CASCADE,
                                     blank=True, null=True)
    responsavel = models.OneToOneField('Responsavel', on_delete=models.CASCADE,
                                       blank=True, null=True)
    secretario = models.OneToOneField('Secretario', on_delete=models.CASCADE,
                                      blank=True, null=True)
    plano_trabalho = models.OneToOneField(
        'planotrabalho.PlanoTrabalho',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    estado_processo = models.CharField(
        max_length=1,
        choices=LISTA_ESTADOS_PROCESSO,
        default='0')
    data_publicacao_acordo = models.DateField(blank=True, null=True)
    codigo_ativacao = models.CharField(max_length=12, unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    prazo = models.IntegerField(default=2)

    def __str__(self):
        return self.user.username


class Historico(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    situacao = models.CharField(
        max_length=1,
        choices=LISTA_ESTADOS_PROCESSO,
        blank=True,
        null=True)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='historico', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
