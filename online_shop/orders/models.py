from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from customers.models import Address, Customer
from products.models import OffCode, Product, CustomerOffCode
from products.templatetags.product_extras import toman_format


class Order(BaseModel):
    class Meta:
        verbose_name = _('Order')

    PAY_STATUSES = [
        (0, _('UnPayed')),
        (1, _('Payed')),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
    )

    off_code = models.ForeignKey(
        OffCode,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    final_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Final Price')
    )

    pay_status = models.IntegerField(
        choices=PAY_STATUSES,
        default=0,
        null=True,
        blank=True,
        verbose_name=_('PAY Status'),
        help_text=_('Pay Status of this Oder!'),
    )

    # todo: validate kon addresesh male customere bashe htmn

    def full_clean(self, exclude=None, validate_unique=True):
        if self.off_code and self.off_code.expire and self.off_code.expire < timezone.now():
            raise ValidationError(_('Your off code is expired!'))
        if self.off_code and self.off_code.min_buy and self.total_price < self.off_code.min_buy:
            raise ValidationError(_(f'This off code minimum buy amount is {intcomma(toman_format(self.off_code.min_buy))}!'))
        if not self.off_code_check():
            raise ValidationError(_('Usable counts of this off code is finished!'))

    # def stock_reducer(self):
    #     for order_item in self.orderitem_set.all():
    #         product = order_item.product
    #         product.stock -= order_item.count
    #         product.save()

    @property
    def total_price(self):
        return sum(self.orderitem_set.all().values_list('final_price', flat=True))

    @property
    def final_price_calculator(self):
        if not self.off_code:
            return self.total_price
        elif self.off_code and self.off_code.type == 'amount':
            return min(self.total_price - min(self.off_code.value, self.off_code.max_amount),
                       0) if self.off_code.max_amount else max(self.total_price - self.off_code.value, 0)
        elif self.off_code and self.off_code.type == 'percentage':
            return self.total_price - min(self.total_price * self.off_code.value / 100,
                                          self.off_code.max_amount) if self.off_code.max_amount else self.total_price - self.total_price * self.off_code.value / 100

    def off_code_check(self):
        if self.off_code:
            if not self.off_code.customeroffcode_set.all():
                return not self.customer.order_set.filter(off_code=self.off_code).count() >= self.off_code.usable_count
            else:
                customer_off_code = CustomerOffCode.objects.get(off_code=self.off_code)
                return not self.customer.order_set.filter(off_code=self.off_code).count() >= customer_off_code.usable_count
        else:
            return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.final_price = self.final_price_calculator
        self.orderitem_set.filter(status=0).update(status=1)
        super().save(force_insert, force_update, using, update_fields)


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
        null=True,
        blank=True,
    )

    status = models.IntegerField(
        choices=STATUSES,
        default=0,
        null=True,
        blank=True,
        verbose_name=_('Status'),
        help_text=_('Status of this Oder Item!'),
    )

    final_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Final Price')
    )

    # def full_clean(self, exclude=None, validate_unique=True):
    #     if self.count > self.product.stock:
    #         raise ValidationError(f'This count of {self.product.name} is not available in store!')

    def __str__(self):
        return f'{self.product} - {self.count}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.final_price = self.final_price_calculator()
        super().save(force_insert, force_update, using, update_fields)

    def final_price_calculator(self):
        return self.product.final_price * self.count

    def price_formatter(self):
        return intcomma(toman_format(self.final_price))

    def order_items_final_price(self):
        return intcomma(toman_format(sum(OrderItem.objects.filter(customer=self.customer, status=0).values_list('final_price', flat=True))))

    @property
    def order_total_price(self):
        return sum(OrderItem.objects.filter(customer=self.customer, status=0).values_list('final_price', flat=True))

    @property
    def order_total_discount(self):
        return f"{round(100 * (1 - (self.order_total_price /OrderItem.objects.filter(customer=self.customer, status=0).annotate(result=F('count') * F('product__price')).aggregate(Sum('result'))['result__sum'])), 2)}%"
