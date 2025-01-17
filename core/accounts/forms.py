from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from .models import User


class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm, self).confirm_login_allowed(user)

        if not user.is_verified:
            raise ValidationError("User is Not Verified!!")


class SignupForm(auth_forms.UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
