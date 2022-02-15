from django.core.exceptions import ValidationError
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
        verbose_name=_('type'),
        help_text=_('This is discount type!'),
    )

    value = models.PositiveIntegerField(
        verbose_name=_('value'),
        help_text=_('This is discount value!'),
    )

    max_amount = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('maximum amount'),
        help_text=_('This is maximum amount for percentage discounts!'),
    )

    expire = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('expire date'),
        help_text=_('This is he discount expire date!'),
    )

    def __str__(self):
        return f'{self.value}%' if self.type == 'percentage' else f'{self.value} Toman'

    # todo: to order checkon validate kon age expiresh gozashte error bde

    def full_clean(self, exclude=None, validate_unique=True):
        if self.type == 'percentage' and not 0 < self.value < 100:
            raise ValidationError(_('Percentage type value must be between 0 & 100.'))


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
        verbose_name=_('Code'),
        help_text=_('This is the code of off code!'),
        unique=True,
    )

    min_buy = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Minimum Buy'),
        help_text=_('This off code could be activate when final price will bigger than minimum buy!'),
    )

    customers = models.ManyToManyField(
        Customer,
        through=CustomerOffCode,
        verbose_name=_('Customers'),
        help_text=_('Customers that can use this off code'),
        null=True,
        blank=True,
    )

    usable_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=1,
        verbose_name=_('Usable Count'),
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
        verbose_name=_(''),
        help_text=_(''),
    )

    value = models.CharField(
        max_length=2555,
        verbose_name=_(''),
        help_text=_(''),
    )


class Product(BaseModel):
    class Meta:
        verbose_name = _('Product')

    name = models.CharField(
        max_length=31,
        verbose_name=_(''),
        help_text=_(''),
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    properties = models.ManyToManyField(
        Property,
        verbose_name=_(''),
        help_text=_(''),
    )

    stock = models.PositiveIntegerField(
        verbose_name=_(''),
        help_text=_(''),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
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


class Comment(BaseModel):
    class Meta:
        verbose_name = _('Comment')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
        verbose_name=_(''),
        help_text=_(''),
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    text = models.TextField(
        verbose_name=_(''),
        help_text=_(''),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        verbose_name=_(''),
        help_text=_(''),
    )
