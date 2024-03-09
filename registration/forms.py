from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'email', )
