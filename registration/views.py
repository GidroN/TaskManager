from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, View, TemplateView

from registration.forms import CustomUserCreationForm, CustomUserAuthenticationForm
from registration.utils import send_email_for_verify


class EmailConfirmView(TemplateView):
    template_name = 'registration/email_verify.html'


class CustomLoginView(LoginView):
    fields = '__all__'
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('today_tasks')
    authentication_form = CustomUserAuthenticationForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('today_tasks')

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email_for_verify(self.request, user)
            return redirect('email-confirm')
        return render(request, 'registration/register.html', {'form': form})


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('today_tasks')

        return redirect('login')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        return user
