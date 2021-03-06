from django.db import models
from financeAwareness.models.category import Category
from financeAwareness.models.transaction import Transaction

class TransactionItem(models.Model):
    item_name = models.CharField(max_length=100)
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name="items", null=True)
    item_value = models.FloatField()
    is_planned = models.BooleanField(default=True,blank=True)

    class Meta:
        db_table = 'transactionItem'
    
    def __str__(self):
        return self.item_name