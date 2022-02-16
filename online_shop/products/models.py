from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
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

    def __add__(self, other):
        if other is None:
            return self
        if self.type == 'percentage' and type(other) == Discount and other.type == 'percentage':
            value = self.value + other.value - (self.value * other.value / 100)
            max_amount = None
            expire = None
            if not self.max_amount and not other.max_amount:
                max_amount = None
            elif self.max_amount and other.max_amount:
                max_amount = min(self.max_amount, other.max_amount)
            elif not self.max_amount:
                max_amount = other.max_amount
            elif not other.max_amount:
                max_amount = self.max_amount
            if not self.expire and not other.expire:
                expire = None
            elif self.expire and other.expire:
                expire = min(self.expire, other.expire)
            elif not self.expire:
                expire = other.expire
            elif not other.expire:
                expire = self.expire
            return Discount(type='percentage', value=value, max_amount=max_amount, expire=expire)

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
        unique=True,
        verbose_name=_('Name'),
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Parent'),
        help_text=_('Parent category of this category!'),
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Discount'),
        help_text=_('Discount for all of this category products!'),
    )

    def __str__(self):
        return self.name

    hidden_discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        editable=False,
        related_name='category_hidden_discount_set',
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.discount != self.hidden_discount:
            for product in self.product_set.all():
                product.category_discount = self.discount
                product.save()
            self.hidden_discount = self.discount
            self.save()
    # todo: methodi k age discount barash set shod bere hame productaye toye in categoryo in discounto bzne
    # todo: age khode producte az qabl dc dasht dc e categoryo ba oon jaam kone


class Brand(BaseModel):
    class Meta:
        verbose_name = _('Brand')

    name = models.CharField(
        max_length=31,
        unique=True,
        verbose_name=_('Name'),
        help_text=_('Name of the brand!'),
    )

    country = models.CharField(
        max_length=31,
        null=True,
        blank=True,
        verbose_name=_('Country'),
        help_text=_('Country of brand!'),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Write description of brand!'),
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Discount'),
        help_text=_('Discount for all products of this brand!'),
    )

    hidden_discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        editable=False,
        related_name='brand_hidden_discount_set',
    )

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.discount != self.hidden_discount:
            for product in self.product_set.all():
                product.brand_discount = self.discount
                product.save()
            self.hidden_discount = self.discount
            self.save()
    # todo: age khode producte az qabl dc dasht dc e categoryo ba oon jaam kone


class Property(BaseModel):
    class Meta:
        verbose_name = _('Property')
        unique_together = ('key', 'value')

    key = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )

    value = models.CharField(
        max_length=2555,
        verbose_name=_('Value'),
        help_text=_('The Value of this title!'),
    )

    def __str__(self):
        return self.key


class Product(BaseModel):
    class Meta:
        verbose_name = _('Product')

    name = models.CharField(
        max_length=31,
        verbose_name=_('Name'),
        unique=True,
    )

    price = models.PositiveIntegerField(
        verbose_name=_('Price'),
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Brand'),
    )

    properties = models.ManyToManyField(
        Property,
        verbose_name=_('Properties'),
        help_text=_('The properties of product!'),
        null=True,
        blank=True,
    )

    stock = models.PositiveIntegerField(
        verbose_name=_('Stock'),
        help_text=_('Count of product that are available in store!'),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        verbose_name=_('Category'),
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Discount'),
        help_text=_('Discount of this product!'),
    )

    category_discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        related_name='category_discount_set',
        null=True,
        blank=True,
        verbose_name=_('Category Discount'),
        help_text=_('The discount of category')
    )

    brand_discount = models.ForeignKey(
        Discount,
        on_delete=models.RESTRICT,
        related_name='brand_discount_set',
        null=True,
        blank=True,
        verbose_name=_('Brand Discount'),
        help_text=_('The discount of Brand')
    )

    def __str__(self):
        return f'{self.name}'

    @property
    def price_after_discounts(self):
        if self.discount and self.discount.expire and self.discount.expire < timezone.now():
            self.discount = None
            self.save()
        if self.category_discount and self.category_discount.expire and self.category_discount.expire < timezone.now():
            self.category_discount = None
            self.save()
        if self.brand_discount and self.brand_discount.expire and self.brand_discount.expire < timezone.now():
            self.brand_discount = None
            self.save()
        if not self.discount and not self.category_discount and not self.brand_discount:
            return self.price
        elif self.discount and (self.category_discount or self.brand_discount):
            total_discount = self.discount + self.category_discount + self.brand_discount
            return min(self.price - self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100
        elif self.category_discount and (self.brand_discount or self.discount):
            total_discount = self.category_discount + self.brand_discount + self.discount
            return min(self.price - self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100
        elif self.brand_discount:
            total_discount = self.brand_discount
            return min(self.price - self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100
        elif self.discount:
            total_discount = self.discount
            return min(self.price - self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100
        elif self.category_discount:
            total_discount = self.category_discount
            return min(self.price - self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100


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
