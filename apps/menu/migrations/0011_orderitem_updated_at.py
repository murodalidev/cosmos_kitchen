# Generated by Django 4.0 on 2022-01-10 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_orderitem_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]
