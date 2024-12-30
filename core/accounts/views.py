from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm


class LoginView(auth_view.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = False
