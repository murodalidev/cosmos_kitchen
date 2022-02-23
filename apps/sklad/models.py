from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Account
from django.db.models.signals import post_save


class Category(models.Model):
    class Meta:
        verbose_name = _('Kategoriya')
        verbose_name_plural = _(' Kategoriyalar')

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    UNIT = (
        (0, _('Kg')),
        (1, _('Litr')),
        (3, _('Dona')),
    )

    class Meta:
        verbose_name = _('Tovar')
        verbose_name_plural = _(' Tovarlar')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Kategoriya'))
    title = models.CharField(max_length=255, verbose_name=_('Nomi'))
    quantity = models.FloatField(default=0, verbose_name=_('Miqdori'))
    unit = models.IntegerField(choices=UNIT, default=0, verbose_name=_('Birligi'))
    is_active = models.BooleanField(default=True, verbose_name=_('Bormi?'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan sanasi'))

    def __str__(self):
        return f'{self.title}'


class ProductOrder(models.Model):
    class Meta:
        verbose_name = _('Kelgan Mahsulot')
        verbose_name_plural = _('Kelgan Mahsulotlar')

    supplier = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Ta\'minlovchi'),
                                 limit_choices_to={'role': 2})
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Kategoriya'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Maxhsulot'))
    quantity = models.FloatField(verbose_name=_('Miqdori'))
    price = models.FloatField(verbose_name=_('Narxi'), null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan sanasi'))

    def __str__(self):
        return f'Kelgan Mahsulot raqami-{self.id}'


class UsedProduct(models.Model):
    class Meta:
        verbose_name = _('Ishlatilgan Mahsulot')
        verbose_name_plural = _('Ishlatilgan Mahsulotlar')

    chef = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Oshpaz'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Kategoriya'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Maxhsulot'))
    quantity = models.FloatField(verbose_name=_('Miqdori'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan sanasi'))

    def __str__(self):
        return f'Ishlatilgan Mahsulot raqami-{self.id}'

    def save(self, *args, **kwargs):
        self.category = self.product.category
        super().save(*args, **kwargs)
    
    


def product_in_post_save(sender, instance, created, *args, **kwargs):
    if created:
        product = Product.objects.get(id=instance.product_id)
        product.quantity += instance.quantity
        product.save()

post_save.connect(product_in_post_save, sender=ProductOrder)


def product_out_post_save(sender, instance, created, *args, **kwargs):
    if created:
        product = Product.objects.get(id=instance.product_id)
        product.quantity -= instance.quantity
        product.save()

post_save.connect(product_out_post_save, sender=UsedProduct)
