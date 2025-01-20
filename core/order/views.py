from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserAddress, Order, OrderItem
from .forms import CheckOutForm
from cart.models import Cart
from cart.cart import CartSession
from .utils import calculate_tax, calculate_shipping
from django.urls import reverse_lazy
from decimal import Decimal


class OrderCheckOutView(LoginRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        address = form.cleaned_data["address_id"]
        coupon = form.cleaned_data["coupon"]
        cart = Cart.objects.get(user=self.request.user)
        cart_items = cart.cart_items.all()
        order = Order.objects.create(
            user=self.request.user,
            title=address.title,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )
        cart_items.delete()
        CartSession(self.request.session).clear()
        total_price = order.calculate_total_price()
        if coupon:
            total_price = total_price - \
                round((total_price * Decimal(coupon.discount_percent / 100)))
            order.coupon = coupon
            coupon.used_by.add(self.request.user)
            coupon.save()

        order.total_price = total_price
        order.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(self.request.POST)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            context['error'] = "کارت پیدا نشد."
            return context

        context['addresses'] = UserAddress.objects.filter(
            user=self.request.user
        )

        total_price = cart.calculate_total_price()
        total_tax = calculate_tax(total_price)
        shipping_cost = calculate_shipping(total_price)

        context['shipping_cost'] = shipping_cost
        context['total_tax'] = total_tax
        context['total_price'] = total_price + total_tax + shipping_cost
        return context


class OrderCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "order/completed.html"
