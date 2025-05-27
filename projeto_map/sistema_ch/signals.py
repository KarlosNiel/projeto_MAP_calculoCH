from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ActivitySubmission, Profile
from django.utils import timezone

HOURS_LIMIT = 80

@receiver(post_save, sender=ActivitySubmission)
def handle_submission_review(sender, instance, created, **kwargs):
    if not created and instance.status == 'APROVADO' and not instance.contabilization:
        profile, _ = Profile.objects.get_or_create(user=instance.user)
        new_total = min(profile.accumulated_hours + instance.hours, HOURS_LIMIT)
        profile.accumulated_hours = new_total
        profile.save()
        instance.contabilization = True
        if instance.reviewed_at is None:
            instance.reviewed_at = timezone.now()
        # evitar recursão infinita
        ActivitySubmission.objects.filter(pk=instance.pk).update(
            contabilization=True, reviewed_at=instance.reviewed_at
        )