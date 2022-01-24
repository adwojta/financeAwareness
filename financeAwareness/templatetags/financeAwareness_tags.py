from itertools import count
from django import template
from ..models import Account
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def available_funds(user):
    sum = Account.objects.filter(user_id=user).aggregate(Sum('value'))
    return sum['value__sum']
    