from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Personnel
from django_countries.widgets import CountrySelectWidget


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = [
            'user', 'last_name', 'first_name', 'email', 'sexe',
            'date_naissance', 'lieu_naissance', 'nationalite',
            'adresse', 'telephone', 'fonction'
        ]
        widgets = {
            'date_naissance': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'adresse': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'nationalite': CountrySelectWidget(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fixer le format du champ date (utile à l'affichage dans certains cas)
        self.fields['date_naissance'].widget.format = '%Y-%m-%d'

        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
            if not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = field.label 



class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )
