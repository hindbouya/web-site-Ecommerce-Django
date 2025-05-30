from django import forms
from django.contrib.auth.models import User

class ModifierCompteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']  # Ici, on permet de modifier le nom et l'email
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }