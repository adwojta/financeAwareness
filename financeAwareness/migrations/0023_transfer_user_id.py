# Generated by Django 3.2 on 2022-01-24 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeAwareness', '0022_auto_20220124_0329'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_transfers', to='auth.user'),
            preserve_default=False,
        ),
    ]
