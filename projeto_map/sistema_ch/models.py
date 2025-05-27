from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class ActivitySubmission(models.Model):
    TYPE_CHOICES = [
        ('WORKSHOP', 'Workshop'),
        ('PALESTRA', 'Palestra'),
        ('CURSO', 'Curso'),
    ]
    STATUS_CHOICES = [
        ('PEDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    archive = models.FileField(upload_to='activities/')
    hours = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PEDENTE')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    contabilization= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accumulated_hours = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.username} - {self.accumulated_hours} hours"
