from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView
from .forms import AdminPasswordChangeForm, AdminProfileEditForm, ProductForm, AdminCouponForm
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib import messages
from shop.models import Product, ProductCategory
from order.models import Coupon
from django.core import exceptions


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


class AdminProfileImageEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    http_method_names = ["post"]
    model = Profile
    fields = ["avatar"]
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "بروزرسانی تصویر پروفایل با موفقیت انجام شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        messages.error(
            self.request, "ارسال تصویر با مشکل مواجه شد! لطفا مجدد تلاش کنید.")
        return redirect(reverse_lazy(self.success_url))


# Start Product CRUD
class AdminProductListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/products/product-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):

        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Product.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except exceptions.FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['categories'] = ProductCategory.objects.all()
        return context


class AdminProductCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/products/product-create.html"
    form_class = ProductForm
    success_message = "محصول جدید با موفقیت افزوده شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-list")


class AdminProductEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    queryset = Product.objects.all()
    template_name = "dashboard/admin/products/product-edit.html"
    form_class = ProductForm
    success_message = "بروزرسانی محصول با موفقیت انجام شد."

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": self.get_object().pk})


class AdminProductDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    queryset = Product.objects.all()
    template_name = "dashboard/admin/products/product-delete.html"
    success_message = "محصول شما با موفقیت حذف گردید."
    success_url = reverse_lazy("dashboard:admin:product-list")

# End Product CRUD


# Start Coupon CRUD
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
