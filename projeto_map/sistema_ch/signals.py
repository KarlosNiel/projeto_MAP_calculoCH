from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submissao, Notificacao

@receiver(post_save, sender=Submissao)
def criar_notificacao_submissao(sender, instance, created, **kwargs):
    if not created:
        old_status = Submissao.objects.filter(pk=instance.pk).values_list('status', flat=True).first()

        if old_status != instance.status and instance.status in ['APROVADO', 'REPROVADO']:
            status_formatado = instance.status.capitalize()
            atividade_nome = instance.atividade.nome

            mensagem = f"Sua submissão para a atividade '{atividade_nome}' foi {status_formatado.lower()}."

            Notificacao.objects.create(
                user=instance.aluno,
                mensagem=mensagem
            )
