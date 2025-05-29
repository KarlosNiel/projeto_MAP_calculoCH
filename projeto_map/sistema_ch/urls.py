from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Para corrigir o erro do base.html
    path('atividades/', views.atividades_publicas, name='atividades_publicas'),  # nome igual à view
    path('dashboard/atividades/', views.dashboard_atividades, name='dashboard_atividades'),
]
