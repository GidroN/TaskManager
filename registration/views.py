from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from app.models import Group
from registration.forms import CustomUserCreationForm, CustomUserAuthenticationForm


def display_account_info(request, user):
    return render(request, 'app/account_page.html', {'user': user})


class CustomLoginView(LoginView):
    fields = '__all__'
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('today_tasks')
    authentication_form = CustomUserAuthenticationForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('today_tasks')

    def form_valid(self, form):
        default_groups = {
            'planned': 'Запланированные задачи',
            'today': 'Задачи на сегодня',
            'overdue': 'Просроченные задачи',
            'all-tasks': 'Все задачи',
        }

        user = form.save()
        if user is not None:
            for slug, name in default_groups.items():
                Group.objects.create(slug=slug, name=name, user=user)

            login(self.request, user)

        return super(RegisterView, self).form_valid(form)

