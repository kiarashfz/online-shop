from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from customers.models import Customer


class BaseDiscount(BaseModel):
    class Meta:
        abstract = True

    TYPES = [
        ('percentage', _('Percentage')),
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
        verbose_name=_('Customer'),
    )

    off_code = models.ForeignKey(
        'OffCode',
        on_delete=models.RESTRICT,
        verbose_name=_('OffCode'),
    )

    usable_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=1,
        verbose_name=_('Usable count'),
        help_text=_('Times that customer can use this off code!'),
    )


class OffCode(BaseDiscount):
    class Meta:
        verbose_name = _('Off Code')

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
        verbose_name_plural = _('Categories')

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.product_set:
            for product in self.product_set.all():
                product.save()

    def __str__(self):
        return self.name

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Category.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

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

    categories = models.ManyToManyField(
        Category,
        verbose_name=_('Categories'),
        help_text=_('Categories of this brand!'),
    )

    @admin.display
    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            '0000FF',
            self.name,
        )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.product_set:
            for product in self.product_set.all():
                product.save()

    def __str__(self):
        return self.name

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
        return f'{self.key}|{self.value}'


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

    final_price = models.PositiveIntegerField(
        verbose_name=_('Final Price'),
        editable=False,
        null=True,
        blank=True,
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Brand'),
    )

    image = models.ImageField(
        null=True,
        blank=True,
        default='products/default_product.jpeg',
        upload_to='products',
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

    def __str__(self):
        return f'{self.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.final_price = self.final_price_calculator
        super().save(force_insert, force_update, using, update_fields)

    def full_clean(self, exclude=None, validate_unique=True):
        if self.discount and self.discount.type == 'amount' and (self.category.discount or self.brand.discount):
            raise ValidationError('You cannot set amount discount when the product has category or brand discount!')

    @property
    def final_price_calculator(self):
        if self.discount and self.discount.expire and self.discount.expire < timezone.now():
            self.discount = None
            self.save()
        if self.category.discount and self.category.discount.expire and self.category.discount.expire < timezone.now():
            self.category.discount = None
            self.save()
        if (self.brand.discount if self.brand else None) and self.brand.discount.expire and self.brand.discount.expire < timezone.now():
            self.brand.discount = None
            self.save()
        if not self.discount and not self.category.discount and not (self.brand.discount if self.brand else None):
            return int(self.price)
        if self.discount and (self.category.discount or (self.brand.discount if self.brand else None)):
            total_discount = self.discount + self.category.discount + (self.brand.discount if self.brand else None)
            return int(self.price - min(self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100)
        elif self.category.discount and ((self.brand.discount if self.brand else None) or self.discount):
            total_discount = self.category.discount + (self.brand.discount if self.brand else None) + self.discount
            return int(self.price - min(self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100)
        elif self.brand and self.brand.discount:
            total_discount = self.brand.discount
            return int(self.price - min(self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100)
        elif self.discount:
            total_discount = self.discount
            return int(self.price - min(self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100)
        elif self.category.discount:
            total_discount = self.category.discount
            return int(self.price - min(self.price * total_discount.value / 100, total_discount.max_amount)) if total_discount.max_amount else int(self.price - self.price * total_discount.value / 100)
        # else:
        #     if self.di
        #     total_discount = self.discount + self.category.discount
        #     return min(self.price - self.price * total_discount.value / 100, total_discount.max_amount) if total_discount.max_amount else self.price - self.price * total_discount.value / 100


class Comment(BaseModel):
    class Meta:
        verbose_name = _('Comment')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
        verbose_name=_('Customer'),
        help_text=_('Customer that this comment is for.'),
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Parent Comment'),
        help_text=_('Comment that you reply it!'),
    )

    text = models.TextField(
        verbose_name=_('Text'),
        help_text=_('Text of your comment!'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        verbose_name=_('Product'),
        help_text=_('Product that this comment is for.'),
    )


class ExtraImage(BaseModel):
    class Meta:
        verbose_name = _('Extra Image')
        verbose_name_plural = _('Extra Images')

    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        verbose_name=_('Product'),
        help_text=_('Product that this image for.')
    )

    image = models.ImageField(
        verbose_name=_('Image')
    )
