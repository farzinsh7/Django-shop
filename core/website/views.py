from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import ContactUsModel
from .forms import ContactFormClass
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(TemplateView):
    template_name = "website/index.html"


class AboutView(TemplateView):
    template_name = "website/about.html"


class ContactView(SuccessMessageMixin, CreateView):
    model = ContactUsModel
    form_class = ContactFormClass
    success_url = reverse_lazy("website:contact")
    template_name = "website/contact.html"
    success_message = "فرم شما با موفقیت ارسال گردید."
