from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ActivitySubmission, Profile
from .registry import get_strategy

@receiver(post_save, sender=ActivitySubmission)
def handle_submission_review(sender, instance, created, **kwargs):
    if not created and instance.status == 'APROVADO' and not instance.contabilization:
        profile, _ = Profile.objects.get_or_create(user=instance.user)

        strategy = get_strategy(instance)
        if not strategy:
            return 

        horas_a_adicionar = strategy.calculate_ch(instance)

        sucesso, _ = profile.add_hours(horas_a_adicionar)

        updated_fields = {
            'contabilization': sucesso,
            'reviewed_at': timezone.now(),
        }

        ActivitySubmission.objects.filter(pk=instance.pk).update(**updated_fields)
