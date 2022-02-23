from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save


ROLE = (
    (0, _('Super foydalanuvchi')),
    (1, _('Ofitsant')),
    (2, _('Ta\'minlovchi')),
)


class AccountManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if phone is None:
            raise ValueError(_('User should have an phone'))
        account = self.model(phone=phone, **extra_fields)
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, phone, password=None, **kwargs):
        if phone is None:
            raise ValueError(_('User should have an phone'))
        account = self.create_user(phone=phone, password=password, **kwargs)
        account.is_superuser = True
        account.is_staff = True
        account.is_active = True
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name=_('Ismi'))
    last_name = models.CharField(max_length=100, verbose_name=_('Familiyasi'))
    phone = models.CharField(max_length=9, unique=True, db_index=True, verbose_name='Raqami*',
                             help_text=_('9 ta raqam bolishi kerak, masalan: 979998877'))
    email = models.EmailField(max_length=50, unique=True, verbose_name=_('Email'), db_index=True, null=True, blank=True)
    telegram_id = models.CharField(null=True, blank=True, verbose_name=_('Telegram ID*'), max_length=10)
    role = models.IntegerField(choices=ROLE, default=1, verbose_name=_('Foydalanuvchi huquqi'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_staff = models.BooleanField(default=True, verbose_name=_('Xodim'))
    is_superuser = models.BooleanField(default=True, verbose_name=_('Super foydalanuvchi'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Yangilangan sanasi'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan sanasi'))

    objects = AccountManager()

    EMAIL_FIELD = 'phone'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.last_name and self.first_name:
            return f'{self.last_name} {self.first_name}'
        return self.phone

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def save(self, *args, **kwargs):
        if self.role == 0:
            self.is_superuser = True
        else:
            self.is_superuser = False
        super().save(*args, **kwargs)

