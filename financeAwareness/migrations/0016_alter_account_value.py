# Generated by Django 3.2 on 2022-01-23 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0015_recurringtransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]