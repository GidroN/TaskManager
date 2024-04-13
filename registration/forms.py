from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя или Email")

    def clean_username(self):
        username_or_email = self.cleaned_data['username']
        user = User.objects.filter(username=username_or_email) or User.objects.filter(email=username_or_email)
        if user and not user[0].is_active:
            raise ValidationError('Ой, кажется вы забыли активировать почту.')
        if not user:
            raise ValidationError('Неправильные данные!')
        return user[0].username


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']