# Generated by Django 4.0 on 2022-01-06 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sklad', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': ' Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': ' Products'},
        ),
    ]
