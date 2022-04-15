from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from django.urls import path

from customers.apis import CustomerCreateApiView, UserCreateApiView, UserListApiView, UserDetailApiView, AddressListApiView, AddressDetailApiView, AddressDeleteApiView, AddressCreateApiView, UserUpdateApiView, CustomerUpdateApiView, AddressUpdateApiView, ConfirmCode
from customers.views import CustomerCreateView, AboutTemplateView, MyLoginView, CustomerDashboardTemplateView

app_name = 'customers'
urlpatterns = [
    path('customer_create_api/', CustomerCreateApiView.as_view(), name='customer_create_api'),
    path('user_create_api/', UserCreateApiView.as_view(), name='user_create_api'),
    path('sign-up/', CustomerCreateView.as_view(), name='sign-up'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('user_list_api_view/', UserListApiView.as_view(), name='user_list_api_view'),
    path('user_detail_api_view/<int:pk>', UserDetailApiView.as_view(), name='user_detail_api_view'),
    path('address_list_api_view/', AddressListApiView.as_view(), name='address_list_api_view'),
    path('address_detail_api_view/<int:pk>', AddressDetailApiView.as_view(), name='address_detail_api_view'),
    path('address_delete_api_view/<int:pk>', AddressDeleteApiView.as_view(), name='address_delete_api_view'),
    path('address_create_api_view', AddressCreateApiView.as_view(), name='address_create_api_view'),
    path('dashboard', CustomerDashboardTemplateView.as_view(), name='dashboard'),
    path('user_update_api_view/<int:pk>', UserUpdateApiView.as_view(), name='user_update_api_view'),
    path('customer_update_api_view/<int:pk>', CustomerUpdateApiView.as_view(), name='customer_update_api_view'),
    path('address_update_api_view/<int:pk>', AddressUpdateApiView.as_view(), name='address_update_api_view'),
    path('confirm_code', ConfirmCode.as_view(), name='confirm_code'),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_change/', PasswordChangeView.as_view(), name='password_change'),
]
