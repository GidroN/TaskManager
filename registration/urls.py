from django.urls import path
from .views import (CustomLoginView, RegisterView, EmailConfirmView, EmailVerifyView, EmailChangeView,
                    EmailSuccessView)

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('email-change/', EmailChangeView.as_view(), name='email-change'),
    path('email-success/', EmailSuccessView.as_view(), name='email-success'),
    path('email-confirm/', EmailConfirmView.as_view(), name='email-confirm'),
    path('email-verify/<uidb64>/<token>/', EmailVerifyView.as_view(), name='email_verify'),

    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirmm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

