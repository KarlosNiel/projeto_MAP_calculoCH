from django.contrib import admin, messages
from .models import ActivitySubmission, Profile
from .registry import get_strategy

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

    def save_model(self, request, obj, form, change):
        if obj.status == 'APROVADO' and not obj.contabilization:
            profile, _ = Profile.objects.get_or_create(user=obj.user)
            strategy = get_strategy(obj)
            if strategy:
                horas = strategy.calculate_ch(obj)
                sucesso, msg = profile.add_hours(horas)
                if sucesso:
                    obj.contabilization = True
                    self.message_user(request, msg, messages.SUCCESS)
                else:
                    obj.contabilization = False
                    self.message_user(request, msg, messages.WARNING)

        super().save_model(request, obj, form, change)
    

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'accumulated_hours')