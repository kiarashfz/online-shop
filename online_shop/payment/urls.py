from django.urls import path
from .views import go_to_gateway_view, callback_gateway_view, pay_unpaid

app_name = 'payment'
urlpatterns = [
    path('payment/', go_to_gateway_view, name='payment'),
    path('pay_unpaid/<int:order_id>', pay_unpaid, name='pay_unpaid'),
    path('callback/', callback_gateway_view, name='callback'),
]

# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('request/', views.send_request, name='request'),
#     path('verify/', views.verify, name='verify'),
# ]
