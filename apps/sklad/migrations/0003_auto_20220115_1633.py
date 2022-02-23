# Generated by Django 3.2.11 on 2022-01-15 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sklad', '0002_alter_category_options_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategoriya', 'verbose_name_plural': ' Kategoriyalar'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Tovar', 'verbose_name_plural': ' Tovarlar'},
        ),
        migrations.AlterModelOptions(
            name='productorder',
            options={'verbose_name': 'Kelgan Mahsulot', 'verbose_name_plural': 'Kelgan Mahsulotlar'},
        ),
        migrations.AddField(
            model_name='productorder',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=7, null=True, verbose_name='Narxi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sklad.category', verbose_name='Kategoriya'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sanasi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Bormi?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.IntegerField(choices=[(0, 'Kg'), (1, 'Litr'), (3, 'Dona')], default=0, verbose_name='Birligi'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sklad.category', verbose_name='Kategoriya'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sanasi'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sklad.product', verbose_name='Maxhsulot'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='quantity',
            field=models.DecimalField(decimal_places=3, max_digits=7, verbose_name='Soni'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='supplier',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 2}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="Ta'minlovchi"),
        ),
    ]
