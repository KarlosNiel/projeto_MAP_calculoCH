from django.contrib import admin
from .models import CustomUser, Atividade, Submissao, Notificacao

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo', 'horas_totais')
    list_filter = ('tipo',)
    search_fields = ('username', 'email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'horas')
    list_filter = ('tipo',)
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Submissao)
class SubmissaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'atividade', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('aluno__username', 'atividade__nome')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('user', 'mensagem', 'created_at')
    search_fields = ('user__username', 'mensagem')
    readonly_fields = ('created_at', 'updated_at')
