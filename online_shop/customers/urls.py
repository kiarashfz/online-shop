from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from django.urls import path

from customers.apis import CustomerCreateApiView, UserCreateApiView, UserListApiView, UserDetailApiView, \
    AddressListApiView, AddressDetailApiView
from customers.views import CustomerCreateView, AboutTemplateView

app_name = 'customers'
urlpatterns = [
    path('customer_create_api/', CustomerCreateApiView.as_view(), name='customer_create_api'),
    path('user_create_api/', UserCreateApiView.as_view(), name='user_create_api'),
    path('sign-up/', CustomerCreateView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(template_name='landing/html&css/html/pages/sign-in.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('user_list_api_view/', UserListApiView.as_view(), name='user_list_api_view'),
    path('user_detail_api_view/<int:pk>', UserDetailApiView.as_view(), name='user_detail_api_view'),
    path('address_list_api_view/', AddressListApiView.as_view(), name='address_list_api_view'),
    path('address_detail_api_view/<int:pk>', AddressDetailApiView.as_view(), name='address_detail_api_view'),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_change/', PasswordChangeView.as_view(), name='password_change'),
]
