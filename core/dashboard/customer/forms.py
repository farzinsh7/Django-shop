from django.contrib.auth.forms import PasswordChangeForm


class CustomerPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_incorrect": _(
            "رمز عبور فعلی شما به درستی وارد نشده است. لطفا دوباره وارد کنید."
        ),
        "password_mismatch": _("فیلدهای رمز عبور جدید با هم برابر نیستند!"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = "form-control"
        self.fields['new_password1'].widget.attrs['class'] = "form-control"
        self.fields['new_password2'].widget.attrs['class'] = "form-control"
        self.fields['old_password'].widget.attrs['placeholder'] = "رمز عبور فعلی را وارد کنید."
        self.fields['new_password1'].widget.attrs['placeholder'] = "رمز عبور جدید را وارد کنید."
        self.fields['new_password2'].widget.attrs['placeholder'] = "مجدد رمز عبور جدید را وارد کنید."
