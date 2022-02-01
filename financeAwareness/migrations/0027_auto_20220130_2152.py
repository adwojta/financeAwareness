# Generated by Django 3.2 on 2022-01-30 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0026_alter_account_is_saving_goal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_income',
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('income', 'Przychód'), ('expense', 'Wydatek'), ('planned', 'Zaplanowana'), ('recurring', 'Stała')], default='income', max_length=20),
            preserve_default=False,
        ),
    ]