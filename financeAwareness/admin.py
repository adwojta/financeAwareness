from django.contrib import admin
from financeAwareness.models.account import Account

from financeAwareness.models.category import Category
from financeAwareness.models.tag import Tag
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem

# Register your models here.

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(Account)
admin.site.register(Tag)

