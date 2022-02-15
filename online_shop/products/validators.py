from django.core.exceptions import ValidationError
from products.models import BaseDiscount
from django.utils.translation import gettext_lazy as _


def validate_discount_type(discount: BaseDiscount):
    if discount.type == 'percentage' and not 0 < discount.value < 100:
        raise ValidationError(_('Percentage type value must be between 0 & 100.'))
