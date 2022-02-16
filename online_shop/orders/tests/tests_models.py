from django.test import TestCase

from customers.models import Customer, Address
from orders.models import OrderItem, Order
from products.models import Product, Discount, Category, OffCode


class OrderTest(TestCase):
    def setUp(self) -> None:
        self.customer1 = Customer.objects.create()
        self.discount1 = Discount.objects.create(type='percentage', value=50)
        self.category1 = Category.objects.create(name='Cars')
        self.discount2 = Discount.objects.create(type='percentage', value=20)
        self.product1 = Product.objects.create(name='Pride', price=10000, stock=7, category=self.category1,
                                               discount=self.discount1)
        self.off_code1 = OffCode.objects.create(code='ababab', usable_count=1, type='percentage', value=20)
        self.address1 = Address.objects.create(province='thr', customer=self.customer1, city='tehran', area='pasdaran'
                                               , avenue='dolat', no=5, postal_code='155662')
        self.order1 = Order.objects.create(customer=self.customer1, address=self.address1, off_code=self.off_code1)
        self.order_item1 = OrderItem.objects.create(product=self.product1, count=3, customer=self.customer1)

    def test_stock_reducer(self):
        self.order1.stock_reducer()
        self.assertEqual(self.product1.stock, 4)








    def test_off_code_check(self):
        self.assertEqual(self.order1.off_code_check(), True)
        self.assertEqual(self.order2.off_code_check(), False)
        self.assertEqual(self.order3.off_code_check(), True)
        self.assertEqual(self.order4.off_code_check(), True)
        self.assertEqual(self.order5.off_code_check(), True)
        self.assertEqual(self.order6.off_code_check(), False)


# self.order2.stock_reducer()
        # self.assertEqual(self.product1.stock, 4)self.order1.stock_reducer()
        # self.assertEqual(self.product1.stock, 4)self.order1.stock_reducer()
        # self.assertEqual(self.product1.stock, 4)


# self.off_code2 = OffCode.objects.create(code='dhdh', usable_count=3, type='percentage', value=40)
        # self.category2 = Category.objects.create(name='Cars2', discount=self.discount1)
        # self.order2 = Order.objects.create(customer=self.customer1, address=self.address1, off_code=self.off_code1)
        # self.order3 = Order.objects.create(customer=self.customer1, address=self.address1, off_code=self.off_code1)
        # self.order4 = Order.objects.create(customer=self.customer1, address=self.address1, off_code=self.off_code2)
        # self.order5 = Order.objects.create(customer=self.customer1, address=self.address1, off_code=self.off_code1)
        # self.order6 = Order.objects.create(customer=self.customer1, address=self.address1, off_code=self.off_code1)
        # self.order_item2 = OrderItem.objects.create(product=self.product1, count=3, order=self.order2, customer=self.customer1)
        # self.product2 = Product.objects.create(name='z4', price=100000, stock=5, category=self.category2,
        #                                        discount=self.discount2)
