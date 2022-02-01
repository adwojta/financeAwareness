# Generated by Django 3.2 on 2022-01-31 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeAwareness', '0031_auto_20220131_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='auth.user'),
            preserve_default=False,
        ),
    ]
