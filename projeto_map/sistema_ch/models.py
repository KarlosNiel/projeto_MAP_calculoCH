from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractUser, Permission, Group
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


class CustomUser(BaseModel, AbstractUser):
    USER_TYPE = [
        ('SECRETARIO', 'Secretário'),
        ('ALUNO', 'Aluno'),
    ]
    tipo = models.CharField(max_length=20, choices=USER_TYPE, default='ALUNO')
    horas_totais = models.PositiveIntegerField(default=0, validators = [MaxValueValidator(80)])

    def is_secretario(self):
        return self.tipo == 'SECRETARIO'
    
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='customuser_groups',related_query_name='customuser')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='customuser_permissions', related_query_name='customuser')
    
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

class Notificacao(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField()

class Submissao(BaseModel):
    STATUS_TYPE = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REPROVADO', 'Reprovado'),
    ]
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissoes')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='submissoes')
    status = models.CharField(max_length=20, choices=STATUS_TYPE, default='PENDENTE')
    notificacao = models.ForeignKey(Notificacao, on_delete=models.CASCADE, related_name='submissoes', null=True, blank=True)

    def aprovar(self, secretario: CustomUser):
        if not secretario.is_secretario():
            raise ValueError("Apenas secretários podem aprovar submissões.")
        
        calculate = self.atividade.get_calculate_ch()
        horas_calculadas = calculate.calculateCH(self.atividade)

        self.status = 'APROVADO'
        self.aluno.horas_totais += horas_calculadas
        self.aluno.save()
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Submissao.objects.get(pk=self.pk).status
            if self.status == 'APROVADO' and old_status != 'APROVADOR':
                raise PermissionDenied("Use o método `aprovar()` para validar submissões!")
            
        super().save(*args, **kwargs)
