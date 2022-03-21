from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="accounts")
    value = models.FloatField(default=0)
    is_cash = models.BooleanField()
    is_saving_goal = models.BooleanField(null=True,blank=True,default=False)
    is_active_saving_goal = models.BooleanField(default=False)
    
    due_date = models.DateField(null=True,blank=True)
    accomplished_date = models.DateField(null=True,blank=True)
    goal_value = models.FloatField(null=True,blank=True)

    class Meta:
        db_table = 'account'
        ordering = ('-accomplished_date',)

    def __str__(self):
        return self.name