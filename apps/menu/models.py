from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save, pre_save
from apps.accounts.models import Account


class Category(models.Model):
    class Meta:
        verbose_name = _('Kategoriya')
        verbose_name_plural = _('Kategoriyalar')

    title = models.CharField(max_length=255, verbose_name=_('Nomi'))
    is_active = models.BooleanField(default=True, verbose_name=_('Bor narsa'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("YAratilgan sanasi"))

    def __str__(self):
        return f'{self.title}'


def image_path(instance, filename):
    return 'meals/%s/%s/%s.jpg' % (instance.category, instance.title, instance.title)


class Meal(models.Model):
    class Meta:
        verbose_name = _('Ovqat')
        verbose_name_plural = _('Ovqatlar')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Kategoriya'), related_name='meals')
    title = models.CharField(max_length=255, verbose_name=_('Nomi'))
    image = models.ImageField(upload_to=image_path, verbose_name=_('Rasmi'), null=True, blank=True)
    cost = models.FloatField(verbose_name=_('Narxi'))
    is_active = models.BooleanField(default=True, verbose_name=_('Bormi'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan sanasi'))

    def __str__(self):
        return f'{self.title}'

    @property
    def get_image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            else:
                return f'{settings.PROD_BASE_URL}{self.image.url}'
        else:
            return '404'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:40px;"/></a>')
        else:
            return '404'


class Order(models.Model):
    STATUS = (
        (0, _('Tugatildi')),
        (1, _('Kutmoqda')),
        (2, _('Qaytarilgan'))
    )

    class Meta:
        verbose_name = _('Zakaz')
        verbose_name_plural = _('Zakazlar')

    waiter = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('Waiter'),
                               limit_choices_to={'role': 1})
    table = models.IntegerField(null=True, verbose_name=_('Table number'))
    status = models.IntegerField(choices=STATUS, default=1, verbose_name=_('Status'))
    payed = models.BooleanField(default=False, verbose_name=_('To\'landi'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    order_id = models.CharField(null=True, blank=True, verbose_name=_('Order ID'), unique_for_date=created_at, max_length=100)

    def __str__(self):
        return f'Zakaz Raqami-{self.id}'

    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total = sum([item.total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.order_items.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    class Meta:
        verbose_name = _('Order Meal')
        verbose_name_plural = _('Order Meal')

    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Meal'))
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Order'),
                              related_name='order_items')
    price = models.FloatField(verbose_name=_('Price'), null=True)
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    total = models.FloatField(verbose_name=_('Total'), null=True)
    is_completed = models.BooleanField(default=False, verbose_name=_('Is completed'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return f'Order item No-{self.id}'

    @property
    def get_total(self):
        return self.total


def order_item_post_save(sender, instance, created, *args, **kwargs):
    if created:
        order = Order.objects.get(id=instance.order_id)
        total_items = instance.quantity * instance.meal.cost
        instance.total = total_items
        instance.price = instance.meal.cost
        order.status = 1
        order.save()
        instance.save()


post_save.connect(order_item_post_save, sender=OrderItem)
