from django.test import TestCase

from products.models import Discount, Category, Product, Brand


class CategoryTest(TestCase):
    # todo: stock har dafe kam mishe ya na

    def setUp(self) -> None:
        self.category1 = Category.objects.create(name='Cars')
        self.product1 = Product.objects.create(name='Pride', price=100000, stock=7, category=self.category1)
        self.discount1 = Discount.objects.create(type='percentage', value=80)
        self.discount2 = Discount.objects.create(type='percentage', value=10)
        self.brand1 = Brand.objects.create(name='BMW')
        self.product2 = Product.objects.create(name='X6', price=2000000000, stock=7, category=self.category1)

    def tests_category_discount(self):
        self.category1.discount = self.discount1
        self.category1.save()
        self.assertEqual(self.product1.final_price, 20000)
        self.brand1.discount = self.discount2
        self.brand1.save()
        self.product2.brand = self.brand1
        self.product2.save()
        self.assertEqual(self.product2.final_price, 360000000)


class CustomerOffCodeTest(TestCase):
    def setUp(self) -> None:
        pass


class BrandTest(TestCase):
    def setUp(self) -> None:
        self.category1 = Category.objects.create(name='Cars')
        self.brand1 = Brand.objects.create(name='BMW')
        self.product1 = Product.objects.create(name='Pride', price=10000, stock=7, category=self.category1,
                                               brand=self.brand1)
        self.discount1 = Discount.objects.create(type='percentage', value=80)

    def tests_category_discount(self):
        self.brand1.discount = self.discount1
        self.brand1.save()
        self.assertEqual(self.product1.brand.discount, self.discount1)


class PropertyTest(TestCase):
    def setUp(self) -> None:
        pass


class ProductTest(TestCase):
    def setUp(self) -> None:
        self.discount1 = Discount.objects.create(type='percentage', value=50)
        self.category1 = Category.objects.create(name='Cars')
        self.category2 = Category.objects.create(name='Cars2', discount=self.discount1)
        self.discount2 = Discount.objects.create(type='percentage', value=20)
        self.product1 = Product.objects.create(name='Pride', price=10000, stock=7, category=self.category1,
                                               discount=self.discount2)
        self.product2 = Product.objects.create(name='z4', price=100000, stock=5, category=self.category2,
                                               discount=self.discount2)
        self.product3 = Product.objects.create(name='z4', price=100000, stock=5, category=self.category2,
                                               discount=self.discount2)
        self.product4 = Product.objects.create(name='z4', price=100000, stock=5, category=self.category2,
                                               discount=self.discount2)
        self.product5 = Product.objects.create(name='z4', price=100000, stock=5, category=self.category2,
                                               discount=self.discount2)
        self.product6 = Product.objects.create(name='z4', price=100000, stock=5, category=self.category2,
                                               discount=self.discount2)
        self.product7 = Product.objects.create(name='z4', price=100000, stock=5, category=self.category2,
                                               discount=self.discount2)

    def test_final_price(self):
        self.assertEqual(self.product1.final_price, 8000)
        self.assertEqual(self.product2.final_price, 40000)
        self.assertEqual(self.product3.final_price, 40000)
        self.assertEqual(self.product4.final_price, 40000)
        self.assertEqual(self.product5.final_price, 40000)
        self.assertEqual(self.product6.final_price, 40000)
        self.assertEqual(self.product7.final_price, 40000)


class DiscountTest(TestCase):
    def setUp(self) -> None:
        self.discount1 = Discount.objects.create(type='percentage', value=200)


class OffCodeTest(TestCase):
    def setUp(self) -> None:
        pass


class CommentTest(TestCase):
    def setUp(self) -> None:
        pass
