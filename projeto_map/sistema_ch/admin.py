from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import User, Atividade, Submissao, Notificacao

# Admin para User personalizado
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações adicionais', {'fields': ('horas_totais',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'horas_totais', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Admin para Atividade
@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'horas', 'created_at', 'deleted_at')
    search_fields = ('nome', 'tipo')
    list_filter = ('tipo',)
    readonly_fields = ('created_at', 'updated_at')

# Admin para Submissao com lógica de aprovação
@admin.register(Submissao)
class SubmissaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'atividade', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('aluno__username', 'atividade__nome')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['aprovar_submissoes']

    def aprovar_submissoes(self, request, queryset):
        aprovadas = 0
        erros = 0
        for submissao in queryset:
            try:
                submissao.aprovar(request.user)  # usa seu método de aprovação
                aprovadas += 1
            except PermissionDenied as e:
                erros += 1
        if aprovadas:
            self.message_user(request, f'{aprovadas} submissão(ões) aprovada(s) com sucesso.', messages.SUCCESS)
        if erros:
            self.message_user(request, f'{erros} submissão(ões) não puderam ser aprovadas.', messages.ERROR)
    aprovar_submissoes.short_description = "Aprovar submissões selecionadas"

# Admin para Notificação
@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'submissao', 'mensagem', 'created_at')
    search_fields = ('aluno__username', 'mensagem')
    readonly_fields = ('created_at', 'updated_at')
