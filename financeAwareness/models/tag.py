from django.db import models

class Tag(models.Model):
    tag_id =  models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tag'