from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="categories")  
    master_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name="subcategories", null=True, blank=True)
    income = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name