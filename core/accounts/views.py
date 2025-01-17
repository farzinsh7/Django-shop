from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm, SignupForm
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import Signer
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect, render
from django.core.signing import BadSignature
from .models import User


signer = Signer()


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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Optional: Require email verification to activate
        user.save()

        # Generate a signed token
        token = signer.sign(user.pk)

        # Send the verification email
        verification_link = self.request.build_absolute_uri(
            reverse('accounts:verify_email', kwargs={'token': token})
        )
        send_mail(
            'Verify Your Email',
            f'Click the link to verify your email: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return redirect(self.success_url)


class VerifyEmailView(View):
    def get(self, request, token, *args, **kwargs):
        try:
            user_id = signer.unsign(token)
            user = User.objects.get(pk=user_id)
            user.is_verified = True
            user.is_active = True
            user.save()
            return render(request, 'accounts/verification_success.html')
        except (BadSignature, User.DoesNotExist):
            return render(request, 'accounts/verification_failed.html')
