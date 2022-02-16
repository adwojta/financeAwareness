from itertools import count
from datetime import date
from django import template

from financeAwareness.models.transaction import Transaction
from ..models import Account
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def available_funds(user):
    sum = Account.objects.filter(user_id=user).aggregate(Sum('value'))

    if not sum['value__sum']:
        sum['value__sum']='0.0'

    return sum['value__sum']

@register.simple_tag
def available_funds_cash(user):
    sum = Account.objects.filter(user_id=user,is_cash=True).aggregate(Sum('value'))

    if not sum['value__sum']:
        sum['value__sum']='0.0'

    return sum['value__sum']

@register.simple_tag
def available_funds_bank(user):
    sum = Account.objects.filter(user_id=user,is_cash=False).aggregate(Sum('value'))

    if not sum['value__sum']:
        sum['value__sum']='0.0'

    return sum['value__sum']

@register.inclusion_tag('views/account/saving_goal_active.html')
def active_goal(user):
    try:
        goal = Account.objects.get(user_id=user,is_active_saving_goal=True)
    except Account.DoesNotExist:
        goal = None
    if goal:
        months = (goal.due_date.year - date.today().year)*12 + (goal.due_date.month - date.today().month)
        if months < 0:
            remaining = False
        elif months > 0:
            remaining = goal.goal_value - goal.value
            remaining = round(remaining/months)
        else:
            remaining = goal.goal_value - goal.value
    else:
        remaining = False

    return {'remaining':remaining,'goal':goal}

@register.inclusion_tag('views/recurring/recurring_next.html')
def reccuring_next(user):
    exists = True
    try:
        recurrings = Transaction.objects.filter(user_id=user,type__in=['recurringExpense','recurringIncome']).order_by('date')[:3]
    except Account.DoesNotExist:
        exists = False


    return {'recurrings':recurrings,'exists':exists}