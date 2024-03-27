from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from app.models import Group
from registration.forms import CustomUserCreationForm, CustomUserAuthenticationForm


@login_required
def display_account_info(request, user):
    if str(request.user) == str(user):
        return render(request, 'app/account_page.html', {'user': user})
    else:
        return redirect('today_tasks', permanent=True)


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

