# Generated by Django 3.2 on 2022-01-23 01:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeAwareness', '0014_alter_transactionitem_is_planned'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringTransaction',
            fields=[
                ('recurring_transaction_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=100)),
                ('is_active', models.BooleanField()),
                ('is_income', models.BooleanField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='financeAwareness.category')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurring', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
