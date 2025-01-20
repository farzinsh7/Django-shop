from django.conf import settings


def calculate_tax(total_price):
    tax_rate = getattr(settings, 'TAX_RATE', 0)  # Default to 0 if not defined
    return round((total_price * tax_rate) / 100)


def calculate_shipping(total_price):
    free_shipping_threshold = getattr(settings, 'FREE_SHIPPING_THRESHOLD', 0)
    shipping_fee = getattr(settings, 'SHIPPING_FEE', 0)

    return 0 if total_price >= free_shipping_threshold else shipping_fee
