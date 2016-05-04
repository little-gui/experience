from __future__ import unicode_literals
import uuid

from django.db import models
from django.contrib.auth.models import User


class Login(models.Model):
    user = models.OneToOneField(User)
    code = models.UUIDField(default=uuid.uuid4)


INSTRUCAO = ((1, 'Ensino Fundamental'), (2, 'Ensino Medio'), 
    (3, 'Ensino Superior'))
ESTADO_CIVIL = ((1, 'Casado'), (2, 'Solteiro'), (3, 'Divorciado'), 
    (4, 'Separado'), (5, 'Amigado'))


class Empregado(models.Model):
    user = models.OneToOneField(User)
    funcao_pretendida = models.CharField(max_length=255, null=True)
    mover = models.CharField(max_length=255, null=True)
    mover_ano = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    nome = models.CharField(max_length=255, null=True)
    nascimento = models.CharField(max_length=255, null=True)
    cep = models.CharField(max_length=255, null=True)
    endereco = models.CharField(max_length=255, null=True)
    bairro = models.CharField(max_length=255, null=True)
    cidade = models.CharField(max_length=255, null=True)
    telefone = models.CharField(max_length=255, null=True)
    celular = models.CharField(max_length=255, null=True)
    instrucao = models.IntegerField(choices=INSTRUCAO, null=True)
    estado_civil = models.IntegerField(choices=ESTADO_CIVIL, null=True)
    filhos_numero = models.CharField(max_length=5, null=True)
    filhos_idade = models.CharField(max_length=255, null=True)
    empresa = models.CharField(max_length=255, null=True)
    responsavel = models.CharField(max_length=255, null=True)
    empresa_telefone = models.CharField(max_length=255, null=True)
    empresa_cidade = models.CharField(max_length=255, null=True)
    empresa_estado = models.CharField(max_length=255, null=True)
    funcao = models.CharField(max_length=255, null=True)
    empresa_admissao = models.CharField(max_length=255, null=True)
    empresa_demissao = models.CharField(max_length=255, null=True)
