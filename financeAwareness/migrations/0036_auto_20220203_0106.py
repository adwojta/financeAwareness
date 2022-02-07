# Generated by Django 3.2 on 2022-02-03 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0035_remove_transaction_next_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='reccuringType',
            field=models.CharField(choices=[('month', 'Miesiąc'), ('quarter', 'Kwartał'), ('year', 'Rok'), ('week', 'tydzień')], default='month', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('income', 'Przychód'), ('expense', 'Wydatek'), ('planned', 'Zaplanowana'), ('recurringExpense', 'Stały wydatek'), ('recurringIncome', 'Stały przychód'), ('transfer', 'Transfer')], max_length=20),
        ),
    ]