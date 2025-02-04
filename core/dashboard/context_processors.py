from order.models import Order, OrderStatus
from review.models import Review, ReviewStatusType


def order_count_processor(request):

    order = Order.objects.filter(status=OrderStatus.processing.value).count()

    return {'order_count': order}


def review_count_processor(request):

    order = Review.objects.filter(
        status=ReviewStatusType.pending.value).count()

    return {'review_count': order}
