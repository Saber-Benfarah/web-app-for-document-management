from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Archive

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = '__all__'

class CustomUserForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label="Password Confirmation")

    class Meta:
        model = CustomUser
        fields = ['username', 'branch', 'role', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirmation'):
            self.add_error('password_confirmation', 'Passwords do not match.')


class UploadCSVForm(forms.Form):
    file = forms.FileField(label='Choisir un fichier CSV')
