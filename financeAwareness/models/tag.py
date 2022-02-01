from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tags")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name