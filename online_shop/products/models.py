from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from customers.models import Customer


class BaseDiscount(BaseModel):
    class Meta:
        abstract = True

    TYPES = [
        ('percentage', _('Percentage')),
        ('amount', _('Amount')),
    ]

    type = models.CharField(
        max_length=15,
        choices=TYPES,
        verbose_name=_(''),
        help_text=_(''),
    )

    max_amount = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    expire = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )


class Discount(BaseDiscount):
    class Meta:
        verbose_name = _('Discount')

    # todo: methode jaam vase discount vase zamani ke ham producte discount dare ham categorysh discount mikhore


class CustomerOffCode(BaseModel):
    class Meta:
        verbose_name = _('Customer Off Code')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
        verbose_name=_(''),
        help_text=_(''),
    )

    off_code = models.ForeignKey(
        'OffCode',
        on_delete=models.RESTRICT,
        verbose_name=_(''),
        help_text=_(''),
    )

    usable_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=1,
        verbose_name=_(''),
        help_text=_(''),
    )


class OffCode(BaseDiscount):
    class Meta:
        verbose_name = _('Off Code')

    code = models.CharField(
        max_length=63,
        verbose_name=_(''),
        help_text=_(''),
        unique=True,
    )

    min_buy = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    customers = models.ManyToManyField(
        Customer,
        through=CustomerOffCode,
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    usable_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=1,
        verbose_name=_(''),
        help_text=_('Usable Count For each customer! Fill it if you want this off code for ALL customers!'),
    )


class Category(BaseModel):
    class Meta:
        verbose_name = _('Category')

    name = models.CharField(
        max_length=31,
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    # todo: methodi k age discount barash set shod bere hame productaye toye in categoryo in discounto bzne


class Brand(BaseModel):
    class Meta:
        verbose_name = _('Brand')

    name = models.CharField(
        max_length=31,
        unique=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    country = models.CharField(
        max_length=31,
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )


class Property(BaseModel):
    class Meta:
        verbose_name = _('Property')

    key = models.CharField(
        max_length=255,
    )

    value = models.CharField(
        max_length=2555,
    )
