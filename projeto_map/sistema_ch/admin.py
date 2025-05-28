from django.contrib import admin, messages
from .models import ActivitySubmission, Profile
from .registry import get_strategy

@admin.register(ActivitySubmission)
class ActivitySubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'hours', 'type', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'contabilization', 'type')
    actions = ['approve_submissions', 'reject_submissions']

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