from itertools import count
from datetime import date
from django import template
from django.shortcuts import get_object_or_404
from ..models import Account
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def available_funds(user):
    sum = Account.objects.filter(user_id=user).aggregate(Sum('value'))
    return sum['value__sum']

@register.inclusion_tag('views/account/saving_goal_active.html')
def active_goal(user):
    try:
        goal = Account.objects.get(user_id=user,is_active_saving_goal=True)
    except Account.DoesNotExist:
        goal = None
    if goal:
        months = (goal.due_date.year - date.today().year)*12 + (goal.due_date.month - date.today().month)
        remaining = goal.goal_value - goal.value
        remaining = round(remaining/months)
    else:
        remaining = False

    return {'remaining':remaining,'goal':goal}