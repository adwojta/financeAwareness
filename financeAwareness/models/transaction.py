from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from financeAwareness.models.account import Account

class Transaction(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="transactions")
    account_id = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="transactions")
    value = models.FloatField()
    is_finished = models.BooleanField(default=True)
    description = models.TextField(null=True,blank=True)
    date = models.DateTimeField()
    is_income = models.BooleanField()
    #photo = models.
    class Meta:
        db_table = 'transaction'
        ordering = ('-date',)

    def __str__(self):
        return self.name

    