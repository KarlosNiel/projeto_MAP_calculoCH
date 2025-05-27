from django.contrib import admin
from .models import ActivitySubmission, Profile

@admin.register(ActivitySubmission)
class ActivitySubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'hours', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status',)
    actions = ['approve_submissions', 'reject_submissions']

    def approve_submissions(self, request, queryset):
        for submission in queryset.filter(status='P'):
            submission.status = 'A'
            submission.save()
        self.message_user(request, "Submissões aprovadas com sucesso.")
    approve_submissions.short_description = "Aprovar submissões selecionadas"

    def reject_submissions(self, request, queryset):
        updated = queryset.filter(status='P').update(status='R')
        self.message_user(request, f"{updated} submissões recusadas.")
    reject_submissions.short_description = "Recusar submissões selecionadas"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'accumulated_hours')