from django.db import models
from django.contrib.auth.models import User

from financeAwareness.models.category import Category

class RecurringTransaction(models.Model):
    recurring_transaction_id =  models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="recurring")
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category")
    name = models.CharField(max_length=100)
    value = models.FloatField()
    description = models.TextField()
    #next_payment = models.DateField()
    type = models.CharField(max_length=100)
    is_active = models.BooleanField()
    is_income = models.BooleanField()

    class Meta:
        db_table = 'recurringTransaction'