# Generated by Django 3.2 on 2022-01-22 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0010_auto_20220122_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='financeAwareness.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='category_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='financeAwareness.category'),
            preserve_default=False,
        ),
    ]