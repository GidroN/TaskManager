from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterView, display_account_info

urlpatterns = [
    path('page/', display_account_info, name='account_info'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]