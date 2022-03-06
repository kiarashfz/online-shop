from core.models import User
from customers.models import Customer
from orders.models import OrderItem
from products.models import Category


def extras(request):
    categories = Category.objects.all()
    parent_categories = Category.objects.filter(parent=None)
    if request.user.id:
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            cart_count = OrderItem.objects.filter(customer=customer).count()
            order_items_products_ids = customer.orderitem_set.filter(status=0).values_list('product', flat=True)
            order_items = customer.orderitem_set.filter(status=0)
            login = True
        except:
            user, customer, cart_count, order_items_products_ids, order_items, login = request.user, None, 0, [], None, False
    elif order_items := request.session.get('order_items', None):
        user, customer = None, None
        cart_count = len(order_items)
        order_items_products_ids = order_items.keys()
        order_items = order_items
        login = False
    else:
        user, customer, cart_count, order_items_products_ids, order_items, login = None, None, 0, [], None, False
    return {
        'categories': categories,
        'parent_categories': parent_categories,
        'user': user,
        'customer': customer,
        'cart_count': cart_count,
        'order_items_products_ids': order_items_products_ids,
        'order_items': order_items,
        'login': login,
    }
