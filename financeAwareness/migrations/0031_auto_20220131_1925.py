# Generated by Django 3.2 on 2022-01-31 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAwareness', '0030_alter_transaction_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='financeAwareness.Tag'),
        ),
    ]
