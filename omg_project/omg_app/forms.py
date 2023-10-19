from django import forms
from .models import AIModel

class AIModelForm(forms.ModelForm):
    class Meta:
        model = AIModel
        fields = ('model_name',)