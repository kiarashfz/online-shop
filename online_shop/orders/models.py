from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


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
