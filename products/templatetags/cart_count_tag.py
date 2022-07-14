from django import template
from products.models import OrderItem

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user=user)
        if qs.exists():
            sum = 0
            for i in range(0, len(qs)):
                sum += qs[i].quantity
            return sum
    return 0