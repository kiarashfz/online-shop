from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from customers.models import Address, Customer
from products.models import OffCode, Product, CustomerOffCode


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

    def full_clean(self, exclude=None, validate_unique=True):
        if self.off_code and self.off_code.expire and self.off_code.expire < timezone.now():
            raise ValidationError(_('Your off code is expired!'))
        if self.off_code and self.off_code.min_buy and self.total_price < self.off_code.min_buy:
            raise ValidationError(_(f'This off code minimum buy amount is {self.off_code.min_buy}!'))
        if not self.off_code_check():
            raise ValidationError(_('Usable counts of this off code is finished!'))

    def stock_reducer(self):
        for order_item in self.orderitem_set.all():
            product = order_item.product
            product.stock -= order_item.count
            product.save()

    @property
    def total_price(self):
        products = self.orderitem_set.all().values_list('product')
        total_price = 0
        for p in products:
            total_price += p.final_price
        return total_price

    @property
    def final_price(self):
        if not self.off_code:
            return self.total_price
        elif self.off_code and self.off_code.type == 'amount':
            return self.total_price - min(self.off_code.value, self.off_code.max_amount) if self.off_code.max_amount else self.total_price - self.off_code.value
        elif self.off_code and self.off_code.type == 'percentage':
            return min(self.total_price - self.total_price * self.off_code.value/100, self.off_code.max_amount) if self.off_code.max_amount else self.total_price - self.total_price * self.off_code.value/100, self.off_code.max_amount

    def off_code_check(self):
        if self.off_code:
            if not self.off_code.customeroffcode_set.all():
                return not len(
                    self.customer.order_set.filter(off_code=self.off_code)) > self.off_code.usable_count
            else:
                customer_off_code = CustomerOffCode.objects.get(off_code=self.off_code)
                return not len(
                    self.customer.order_set.filter(off_code=self.off_code)) > customer_off_code.usable_count
        else:
            return True
# todo: ba har order az stocke oon product kam she


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
        verbose_name=_('Product'),
        help_text=_('Product of Order Item!'),
    )

    count = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Count'),
        help_text=_('Count of product for Order Item!'),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_('Order'),
        help_text=_('The order that this Order Item is for!'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
        verbose_name=_('Customer'),
        help_text=_('Customer of this Order Item!'),
    )

    status = models.IntegerField(
        choices=STATUSES,
        default=0,
        null=True,
        blank=True,
        verbose_name=_('Status'),
        help_text=_('Status of this Oder Item!'),
    )

    def full_clean(self, exclude=None, validate_unique=True):
        if self.count > self.product.stock:
            raise ValidationError(f'This count of {self.product.name} is not available in store!')
