# Generated by Django 3.2 on 2022-01-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0012_alter_transaction_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionitem',
            old_name='name',
            new_name='item_name',
        ),
        migrations.RenameField(
            model_name='transactionitem',
            old_name='value',
            new_name='item_value',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='value',
            field=models.FloatField(),
        ),
    ]