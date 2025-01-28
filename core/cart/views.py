from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from .cart import CartSession
from shop.models import ProductCategory, Product
from django.shortcuts import get_object_or_404
from django.contrib import messages


class SessionAddProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")

        if product_id:
            product = get_object_or_404(Product, id=product_id)

            if product.stock <= 0:
                return JsonResponse({
                    "error": True,
                    "messages": ["محصول انتخابی شما فاقد موجودی می باشد."]
                }, status=400)

        # Check if the cart already has this product and the quantity exceeds stock
            product_in_cart = next((item for item in cart.get_cart_dict()[
                                   "items"] if item["product_id"] == str(product.id)), None)
            if product_in_cart and product_in_cart["quantity"] >= product.stock:
                return JsonResponse({
                    "error": True,
                    "messages": ["موجودی محصول در سبد خرید شما بیشتر از موجودی انبار است."]
                }, status=400)

            cart.add_product(product_id)

        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionRemoveProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.remove_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionUpdateProductQuantityView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        if product_id and quantity:
            cart.update_product_quantity(product_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class CartSummaryView(TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        context["cart_items"] = cart_items
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_amount"] = cart.get_total_payment_amount()
        return context
