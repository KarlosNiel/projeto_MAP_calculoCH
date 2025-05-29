from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ActivitySubmissionForm
from .models import ActivitySubmission, Profile

def index(request):
    return render(request, 'atividades_publicas.html')

def atividades_publicas(request):
    return render(request, 'atividades_publicas.html')

# Dashboard protegida (requer login)
@login_required
def dashboard_atividades(request):
    # Cria perfil do usuário se não existir
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Processa o envio do formulário
    if request.method == 'POST':
        form = ActivitySubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.user = request.user
            atividade.save()
            messages.success(request, 'Atividade enviada com sucesso! Aguarde a validação.')
            return redirect('dashboard_atividades')
    else:
        form = ActivitySubmissionForm()

    # Lista as submissões do usuário autenticado
    submissions = ActivitySubmission.objects.filter(user=request.user).order_by('-submitted_at')

    # Cálculo da barra de progresso (80h)
    progresso = int((profile.accumulated_hours / 80) * 100)

    return render(request, 'atividades.html', {
        'form': form,
        'submissions': submissions,
        'profile': profile,
        'progresso': progresso,
    })
