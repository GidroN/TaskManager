from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView


def display_account_info(request):
    return render(request, 'app/account_page.html', {'user': request.user})


class CustomLoginView(LoginView):
    fields = '__all__'
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('today_tasks')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('today_tasks')

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)

