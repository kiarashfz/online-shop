from django.core.exceptions import ValidationError
from products.models import BaseDiscount


def discount_type_validator(discount: BaseDiscount):
    if discount.type == 'percentage' and not 0 < discount.value < 100:
        raise ValidationError('Percentage type value must be between 0 & 100.')
