from datetime import datetime
import os
from django.db import models
from django.contrib.auth.models import User
from financeAwareness.models.tag import Tag

from financeAwareness.models.account import Account

def upload(instance,filename):
    extension = filename.split('.',1)[1]
    return 'user/{0}/{1}.{2}'.format(instance.user_id,datetime.now(),extension)

class Transaction(models.Model):
    types=(('income','Przychód'),('expense','Wydatek'),('planned','Zaplanowana'),('recurringExpense','Stały wydatek'),('recurringIncome','Stały przychód'),('transfer','Transfer'))
    reccuringTypes=(('month','Miesiąc'),('quarter','Kwartał'),('year','Rok'),('week','Tydzień'))

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="transactions")
    account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="transactions")    
    value = models.FloatField()
    description = models.TextField(null=True,blank=True)
    date = models.DateField()  
    type = models.CharField(choices=types,max_length=16)
    tags = models.ManyToManyField(Tag,related_name='tags',blank=True)

    transfer_account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="transfer",null=True,blank=True)

    recurring_type = models.CharField(choices=reccuringTypes,max_length=7,null=True)
    image = models.ImageField(upload_to=upload,blank=True,null=True)

    class Meta:
        db_table = 'transaction'
        ordering = ('-date',)

    def __str__(self):
        return self.name

    def delete(self):
        try:
            os.unlink(self.image.path)
        except:
            pass
        finally:
            super(Transaction,self).delete()

    

    