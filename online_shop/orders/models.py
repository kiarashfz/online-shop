from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from customers.models import Address, Customer
from products.models import OffCode, Product


class Order(BaseModel):
    class Meta:
        verbose_name = _('Order')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.RESTRICT,
    )

    off_code = models.ForeignKey(
        OffCode,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    # todo: validate kon addresesh male customere bashe htmn


#     def off_code_check(self):
#         if self.off_code.usable_count:
#             return False if len(
#                 self.customer.order_set.filter(off_code=self.off_code)) > self.off_code.usable_count else True
#         else:
#             customer_off_code = CustomerOffCode.objects.get(off_code=self.off_code)
#             return False if len(
#             self.customer.order_set.filter(off_code=self.off_code)) > customer_off_code.usable_count
# todo: ba har order az tocke oon product kam she

class OrderItem(BaseModel):
    class Meta:
        verbose_name = _('Order Item')

    STATUSES = [
        (0, _('Selected')),
        (1, _('Ordered')),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        verbose_name=_(''),
        help_text=_(''),
    )

    count = models.PositiveIntegerField(
        default=1,
        verbose_name=_(''),
        help_text=_(''),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
        verbose_name=_(''),
        help_text=_(''),
    )

    status = models.IntegerField(
        choices=STATUSES,
        default=0,
        null=True,
        blank=True,
        verbose_name=_(''),
        help_text=_(''),
    )
