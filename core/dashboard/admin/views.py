from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from .forms import AdminPasswordChangeForm, AdminProfileEditForm
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile


class AdminDashboardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):

    template_name = "dashboard/admin/home.html"


class AdminSecurityEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "dashboard/admin/profile/security-edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message = "رمز عبور شما با موفقیت تغییر پیدا کرد."


class AdminProfileEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/profile/profile-edit.html"
    form_class = AdminProfileEditForm
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "بروزرسانی با موفقیت انجام شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
