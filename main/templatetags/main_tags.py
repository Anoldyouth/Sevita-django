from django import template
from main.models import *

register = template.Library()


@register.simple_tag(name='get_products')
def get_products(filter=None):
    if not filter:
        return Product.objects.all()
    else:
        return Product.objects.filter(pk=filter)


@register.filter(name='cut')
def cut(products, count):
    if count:
        db_amount = products.count()
        if db_amount >= count:
            products = products.filter(pk__gte=db_amount - count + 1)

    return products


@register.filter(name='user_in')
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False


register.filter('cut', cut)
register.filter('user_in', user_in)
