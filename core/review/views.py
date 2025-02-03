from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Review
from .forms import SubmitReviewForm
from django.contrib import messages


class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Review
    template_name = "review/submit-review.html"
    form_class = SubmitReviewForm

    def form_valid(self, form):
        product = form.cleaned_data['product']
        messages.success(
            self.request, "دیدگا شما با موفقیت ثبت شد و پس از بررسی نمایش داده می شود.")
        return redirect(reverse_lazy("shop:product-detail", kwargs={"slug": product.slug}))

    def form_invalid(self):
        messages.error(
            self.request, "خطایی در هنگام ثبت دیدگاه رخ داده است. مجدد تلاش کنید.")
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_queryset(self):
        return Review.objects.all()
