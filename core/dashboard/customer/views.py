from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, UpdateView, DeleteView
from dashboard.permissions import HasCustomerAccessPermission
from .forms import CustomerPasswordChangeForm, CustomerProfileEditForm, UserAddressForm
from accounts.models import Profile
from django.contrib import messages
from django.shortcuts import redirect
from order.models import UserAddress
from django.core import exceptions
from order.models import Order


class CustomerDashboardHomeView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):

    template_name = "dashboard/customer/home.html"


class CustomerSecurityEditView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "dashboard/customer/profile/security-edit.html"
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    success_message = "رمز عبور شما با موفقیت تغییر پیدا کرد."


class CustomerProfileEditView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/customer/profile/profile-edit.html"
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "بروزرسانی با موفقیت انجام شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class CustomerProfileImageEditView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    http_method_names = ["post"]
    model = Profile
    fields = ["avatar"]
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "بروزرسانی تصویر پروفایل با موفقیت انجام شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        messages.error(
            self.request, "ارسال تصویر با مشکل مواجه شد! لطفا مجدد تلاش کنید.")
        return redirect(reverse_lazy(self.success_url))


class CustomerAddressCreateView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/customer/address/address-create.html"
    form_class = UserAddressForm
    success_message = "آدرس با موفقیت ثبت گردید."

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:customer:address-edit", kwargs={"pk": form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-list")


class CustomerAddressListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = "dashboard/customer/address/address-list.html"

    def get_queryset(self):
        queryset = UserAddress.objects.filter(user=self.request.user)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except exceptions.FieldError:
                pass
        return queryset


class CustomerAddressEditView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/customer/address/address-edit.html"
    form_class = UserAddressForm
    success_message = "آدرس با موفقیت ویرایش گردید."

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-list")


class CustomerAddressDeleteView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/customer/address/address-delete.html"
    success_message = "آدرس انتخابی با موفقیت حذف گردید."
    success_url = reverse_lazy("dashboard:customer:address-list")

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class CustomerOrdersListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = "dashboard/customer/orders/order-list.html"

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            'order_items__product').filter(user=self.request.user)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except exceptions.FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_orders'] = self.get_queryset().count()
        return context
