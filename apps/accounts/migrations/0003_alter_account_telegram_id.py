# Generated by Django 4.0 on 2022-01-05 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Telegram ID*'),
        ),
    ]
