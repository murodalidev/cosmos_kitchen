# Generated by Django 4.0 on 2022-01-07 06:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique_for_date=models.DateTimeField(auto_now_add=True, verbose_name='Created at'), verbose_name='Order ID'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=1, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.IntegerField(blank=True, null=True, verbose_name='Table number'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Updated at'),
            preserve_default=False,
        ),
    ]
