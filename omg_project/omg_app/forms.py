from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AIModel

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class AIModelForm(forms.ModelForm):
    class Meta:
        model = AIModel
        fields = '__all__'