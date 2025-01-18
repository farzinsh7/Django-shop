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
from django.utils.translation import gettext_lazy as _


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
            user.save()
            return render(request, 'accounts/verification_success.html')
        except (BadSignature, User.DoesNotExist):
            return render(request, 'accounts/verification_failed.html')


class PasswordResetView(SuccessMessageMixin, auth_view.PasswordResetView):
    email_template_name = "accounts/email/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    template_name = "accounts/password_reset_form.html"
    title = _("بازیابی رمز عبور")
    success_message = "لینک بازیابی به ایمیل شما ارسال شد."


class PasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"
    title = _("Password reset sent")


class PasswordResetConfirmView(SuccessMessageMixin, auth_view.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"
    title = _("رمز عبور جدید را وارد نمایید.")


class PasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
    title = _("رمز عبور شما با موفقیت تغغیر یافت.")
