# Generated by Django 3.2 on 2022-02-03 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0037_alter_transaction_reccuringtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reccuringType',
            field=models.CharField(choices=[('month', 'Miesiąc'), ('quarter', 'Kwartał'), ('year', 'Rok'), ('week', 'tydzień')], max_length=20, null=True),
        ),
    ]
