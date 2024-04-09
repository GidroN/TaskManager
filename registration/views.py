from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, View, TemplateView

from registration.forms import CustomUserCreationForm, CustomUserAuthenticationForm, EmailChangeForm
from registration.utils import send_email_for_verify


class EmailConfirmView(TemplateView):
    template_name = 'registration/email_verify.html'


class EmailSuccessView(TemplateView):
    template_name = 'registration/email_success.html'


class LinkRestErrorView(TemplateView):
    template_name = 'registration/link_error.html'


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

    def form_valid(self, form):
        user = form.save()
        cache.set(user.username, {'come_from': 'register'})
        send_email_for_verify(self.request, user)
        return redirect('email-confirm')


class EmailVerifyView(View):
    def get(self, request, uidb64, token):

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            cached_user = cache.get(user.username)

            match cached_user.get('come_from'):
                case 'register':
                    user.is_active = True
                case 'email_change':
                    email = cached_user.get('email')
                    user.email = email

            user.save()
            cache.delete(user.username)
            return redirect('email-success')

        return redirect('link-error')


class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/email_change.html'
    success_url = reverse_lazy('email-confirm')
    form_class = EmailChangeForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            user = self.request.user
            cache.set(user.username, {'come_from': 'email_change', 'email': email})
            send_email_for_verify(self.request, user)
            return redirect(self.get_success_url())
        else:
            form.add_error('email', 'Этот адрес уже занят!')

        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def dispatch(self, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and not token_generator.check_token(user, token):
            return redirect('link-error')

        return super().dispatch(*args, **kwargs)
