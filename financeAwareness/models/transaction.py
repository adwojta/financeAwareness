from django.db import models
from django.contrib.auth.models import User
from financeAwareness.models.tag import Tag

from financeAwareness.models.account import Account

class Transaction(models.Model):
    types=(('income','Przychód'),('expense','Wydatek'),('planned','Zaplanowana'),('recurringExpense','Stały wydatek'),('recurringIncome','Stały przychód'),('transfer','Transfer'))
    reccuringTypes=(('month','Miesiąc'),('quarter','Kwartał'),('year','Rok'),('week','tydzień'))

    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="transactions")
    account_id = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="transactions")    
    value = models.FloatField()
    description = models.TextField(null=True,blank=True)
    date = models.DateField()  
    type = models.CharField(choices=types,max_length=20)
    tags = models.ManyToManyField(Tag,related_name='tags',blank=True)

    #Transfer field
    transfer_account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="transfer",null=True,blank=True)

    reccuring_type = models.CharField(choices=reccuringTypes,max_length=20,null=True)
    #receipt = models.

    class Meta:
        db_table = 'transaction'
        ordering = ('-date',)

    def __str__(self):
        return self.name

    