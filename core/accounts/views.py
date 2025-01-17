from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm, SignupForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class LoginView(auth_view.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = False


class LogoutView(auth_view.LogoutView):
    pass


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = SignupForm
    template_name = 'accounts/register.html'
    success_message = "ثبت نام شما با موفقیت انجام شد"
    success_url = reverse_lazy("website:index")
