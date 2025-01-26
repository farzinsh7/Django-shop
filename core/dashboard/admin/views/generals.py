from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from dashboard.permissions import HasAdminAccessPermission
from django.utils.translation import gettext_lazy as _


class AdminDashboardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):

    template_name = "dashboard/admin/home.html"
