# Generated by Django 3.2 on 2022-01-21 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0005_alter_transaction_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_income',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='transaction_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='financeAwareness.transaction'),
        ),
    ]
