from django.urls import path
from .views import go_to_gateway_view, callback_gateway_view

app_name = 'payment'
urlpatterns = [
    path('payment/', go_to_gateway_view, name='payment'),
    path('callback/', callback_gateway_view, name='callback'),
]

# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('request/', views.send_request, name='request'),
#     path('verify/', views.verify, name='verify'),
# ]
