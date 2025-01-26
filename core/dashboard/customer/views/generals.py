from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, UpdateView, DeleteView
from dashboard.permissions import HasCustomerAccessPermission
from dashboard.customer.forms import CustomerPasswordChangeForm, CustomerProfileEditForm, UserAddressForm
from accounts.models import Profile
from django.contrib import messages
from django.shortcuts import redirect
from order.models import UserAddress
from django.core import exceptions
from order.models import Order


class CustomerDashboardHomeView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):

    template_name = "dashboard/customer/home.html"
