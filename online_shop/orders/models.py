from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from customers.models import Address, Customer
from products.models import OffCode


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
