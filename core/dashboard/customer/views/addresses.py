from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, UpdateView, DeleteView
from dashboard.permissions import HasCustomerAccessPermission
from dashboard.customer.forms import UserAddressForm
from django.shortcuts import redirect
from order.models import UserAddress
from django.core import exceptions


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
