from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from registration.forms import CustomUserCreationForm, CustomUserAuthenticationForm


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
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')  # Автоматический вход для пользователя
        return super(RegisterView, self).form_valid(form)


class EmailVerify(View):
    