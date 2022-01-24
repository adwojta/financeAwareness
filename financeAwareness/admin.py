from django.contrib import admin
from financeAwareness.models.account import Account

from financeAwareness.models.category import Category
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem
from financeAwareness.models.transfer import Transfer

# Register your models here.

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(Account)
admin.site.register(Transfer)

