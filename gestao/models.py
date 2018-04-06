import datetime

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from adesao.models import Municipio
from adesao.models import Usuario

TIPOS_DILIGENCIA = (
    ('geral', 'Geral'),
    ('componente', 'Específica'),)


class Diligencia(models.Model):
    texto_diligencia = models.TextField(max_length=200)
    classificacao_arquivo = models.ForeignKey('planotrabalho.SituacoesArquivoPlano',
                                              on_delete=models.CASCADE,
                                              null=True, blank=True)
    data_criacao = models.DateField(default=datetime.date.today)
    ente_federado = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    componente_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    componente_id = models.PositiveIntegerField()
    componente = GenericForeignKey('componente_type', 'componente_id')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_diligencia = models.CharField(
            max_length=10,
            choices=TIPOS_DILIGENCIA)

    def __str__(self):
        return str(self.id)