# Generated by Django 3.2 on 2022-01-24 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0020_alter_account_is_saving_goal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('date', models.DateField()),
                ('from_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='from_account', to='financeAwareness.account')),
                ('to_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='to_account', to='financeAwareness.account')),
            ],
        ),
    ]
