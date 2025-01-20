from django.shortcuts import render
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserAddress, Order, OrderItem, Coupon
from .forms import CheckOutForm
from cart.models import Cart
from cart.cart import CartSession
from .utils import calculate_tax, calculate_shipping
from django.urls import reverse_lazy
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone


class OrderCheckOutView(LoginRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
        coupon = cleaned_data['coupon']

        cart = Cart.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)
        total_price = order.calculate_total_price()
        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        return super().form_valid(form)

    def create_order(self, address):
        return Order.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )

    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            discount_amount = round(
                (total_price * Decimal(coupon.discount_percent / 100)))
            total_price -= discount_amount

            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()

        total_tax = calculate_tax(total_price)
        total_price = total_price + total_tax
        shipping_cost = calculate_shipping(total_price)
        total_price += shipping_cost

        order.total_price = total_price

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
        total_price += total_tax
        shipping_cost = calculate_shipping(total_price)

        context['shipping_cost'] = shipping_cost
        context['total_tax'] = total_tax
        context['total_price'] = total_price + shipping_cost
        return context


class OrderCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "order/completed.html"


class OrderValidateCouponView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        user = self.request.user

        status_code = 200
        message = "کد تخفیف با موفقیت ثبت شد."

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return JsonResponse({"message": "کد تخفیف معتبر نمی باشد."}, status=404)

        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, "خطای محدودیت در تعداد استفاده"

            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code, message = 403, "کد تخفیف منقضی شده است"

            elif user in coupon.used_by.all():
                status_code, message = 403, "این کد تخفیف قبلا توسط شما استفاده شده است."

            else:
                cart = Cart.objects.get(user=self.request.user)
                total_price = cart.calculate_total_price()
                total_price = total_price - \
                    round(total_price * (coupon.discount_percent / 100))
                total_tax = calculate_tax(total_price)
                total_price += total_tax
                shipping_cost = calculate_shipping(total_price)
                total_price += shipping_cost
                if shipping_cost == 0:
                    shipping_cost = "رایگان"

        return JsonResponse({
            "message": message,
            "shipping_cost": shipping_cost,
            "total_tax": total_tax,
            "total_price": total_price
        }, status=status_code)
