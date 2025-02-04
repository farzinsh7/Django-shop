from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DeleteView
from dashboard.admin.forms import AdminReviewForm
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from django.core import exceptions
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from review.models import Review


class AdminReviewListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/reviews/review-list.html"

    def get_queryset(self):
        queryset = Review.objects.all()
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


class AdminReviewEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    queryset = Review.objects.all()
    template_name = "dashboard/admin/reviews/review-edit.html"
    form_class = AdminReviewForm
    success_message = "بروزرسانی دیدگاه با موفقیت انجام شد."

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:review-edit", kwargs={"pk": self.get_object().pk})


class AdminReviewDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    success_message = "دیدگاه شما با موفقیت حذف گردید."
    success_url = reverse_lazy("dashboard:admin:review-list")

    def get_queryset(self):
        return Review.objects.all()
