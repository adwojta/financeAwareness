# Generated by Django 3.2 on 2022-01-21 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0008_auto_20220121_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='master_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='financeAwareness.category'),
        ),
    ]
