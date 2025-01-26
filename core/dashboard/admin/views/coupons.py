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


class AdminCouponListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/coupons/coupon-list.html"

    def get_queryset(self):
        queryset = Coupon.objects.all()
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
        context['now'] = timezone.now()
        return context


class AdminCouponCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/coupons/coupon-create.html"
    form_class = AdminCouponForm
    success_message = "کوپن جدید با موفقیت افزوده شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:coupon-edit", kwargs={"pk": form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-list")


class AdminCouponEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    queryset = Coupon.objects.all()
    template_name = "dashboard/admin/coupons/coupon-edit.html"
    form_class = AdminCouponForm
    success_message = "بروزرسانی کوپن با موفقیت انجام شد."

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-edit", kwargs={"pk": self.get_object().pk})


class AdminCouponDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    queryset = Coupon.objects.all()
    template_name = "dashboard/admin/coupons/coupon-delete.html"
    success_message = "کوپن شما با موفقیت حذف گردید."
    success_url = reverse_lazy("dashboard:admin:coupon-list")
