from django.db import models
from django.contrib.auth.models import User
from financeAwareness.models.account import Account

class Transfer(models.Model):
    value = models.FloatField(default=0)
    date = models.DateField()
    from_account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="from_account")
    to_account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="to_account")
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_transfers")

    class Meta:
        db_table = 'transfer'
        ordering = ('-date',)
    
    def __str__(self):
        return "Transfer z dnia " + str(self.date)