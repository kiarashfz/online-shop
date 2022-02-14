from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from customers.models import Customer


class BaseDiscount(BaseModel):
    TYPES = [
        ('percentage', _('Percentage')),
        ('amount', _('Amount')),
    ]

    class Meta:
        abstract = True

    type = models.CharField(
        max_length=15,
        choices=TYPES,
    )

    max_amount = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    expire = models.DateTimeField(
        null=True,
        blank=True,
    )


class Discount(BaseDiscount):
    pass


class CustomerOffCode(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
    )

    off_code = models.ForeignKey(
        'OffCode',
        on_delete=models.RESTRICT,
    )

    usable_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=1,
    )


class OffCode(BaseDiscount):
    code = models.CharField(
        max_length=63,
    )

    min_buy = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    customers = models.ManyToManyField(
        Customer,
        through=CustomerOffCode,
        null=True,
        blank=True,
    )
