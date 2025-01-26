from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm, ProductForm, AdminCouponForm
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib import messages
from shop.models import Product, ProductCategory
from order.models import Coupon
from django.core import exceptions
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AdminDashboardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):

    template_name = "dashboard/admin/home.html"
