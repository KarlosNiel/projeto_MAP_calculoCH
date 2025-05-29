from django import forms
from .models import ActivitySubmission

class ActivitySubmissionForm(forms.ModelForm):
    class Meta:
        model = ActivitySubmission
        fields = ['title', 'type', 'hours', 'archive']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da Atividade'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Horas solicitadas'}),
            'archive': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Descrição da Atividade',
            'type': 'Categoria da Atividade',
            'hours': 'Carga Horária Solicitada',
            'archive': 'Arquivo',
        }
