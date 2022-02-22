from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from django.urls import path

from customers.apis import CustomerCreateApiView, UserCreateApiView
from customers.views import CustomerCreateView, AboutTemplateView

app_name = 'customers'
urlpatterns = [
    path('customer_create_api/', CustomerCreateApiView.as_view(), name='customer_create_api'),
    path('user_create_api/', UserCreateApiView.as_view(), name='user_create_api'),
    path('sign-up/', CustomerCreateView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(template_name='landing/html&css/html/pages/sign-in.html'), name='login'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('logout/', LogoutView.as_view(), {'next_page': 'landing/html&css/html/pages/pricing.html'}, name='logout'),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_change/', PasswordChangeView.as_view(), name='password_change'),
]
