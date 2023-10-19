from django import forms
from .models import AIModel, Data

class AIModelForm(forms.ModelForm):
    class Meta:
        model = AIModel
        fields = '__all__'
        
class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = '__all__'