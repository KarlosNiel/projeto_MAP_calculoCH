from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractUser
from .calculateCH import *

# Create your models here.
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super().delete()

class User(AbstractUser):
    horas_totais = models.PositiveIntegerField(default=0)


class Atividade(BaseModel):
    ATIVIDADE_TYPE = [
        ('WORKSHOP', 'Workshop'),
        ('PALESTRA', 'Palestra'),
        ('CURSO', 'Curso'),
    ]
    CALCULATE_CH_TYPE = {
        'WORKSHOP': CalculateWorkshopCH(),
        'PALESTRA': CalculatePalestraCH(),
        'CURSO': CalculateCursoCH(),
    }
    arquivo = models.FileField(upload_to='atividades/')
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=ATIVIDADE_TYPE, default='WORKSHOP')
    descricao = models.TextField()
    horas = models.PositiveIntegerField()

    def get_calculate_ch(self):
        return self.CALCULATE_CH_TYPE[self.tipo]

class Submissao(BaseModel):
    STATUS_TYPE = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REPROVADO', 'Reprovado'),
    ]
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissoes')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='submissoes')
    status = models.CharField(max_length=20, choices=STATUS_TYPE, default='PENDENTE')

    def aprovar(self, secretario: User):
        if self.status != 'APROVADO':
            self.status = 'APROVADO'

        calculate = self.atividade.get_calculate_ch()
        horas_calculadas = calculate.calculateCH(self.atividade)

        self.aluno.horas_totais += horas_calculadas
        self.aluno.save()
        self.save()

class Notificacao(BaseModel):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    submissao = models.ForeignKey(Submissao, on_delete=models.CASCADE, related_name='notificacoes', null=True, blank=True)
    mensagem = models.TextField()
