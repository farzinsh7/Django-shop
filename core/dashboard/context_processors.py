from order.models import Order, OrderStatus


def order_count_processor(request):

    order = Order.objects.filter(status=OrderStatus.processing.value).count()

    return {'order_count': order}
