from django import forms
from django.contrib.auth.forms import UserCreationForm
from core_auth.models import User


class RegisterForm(UserCreationForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Buat password aman'
            }
        )
    )

    password2 = forms.CharField(
        label='Ulangi Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ulangi password'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]