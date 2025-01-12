from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import AdminPasswordChangeForm
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin


class AdminDashboardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):

    template_name = "dashboard/admin/home.html"


class AdminSecurityEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "dashboard/admin/profile/security-edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message = "رمز عبور شما با موفقیت تغییر پیدا کرد."
