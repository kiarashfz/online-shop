from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import User
from customers.models import Address, Customer


class UserForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['phone', 'password1', 'password2', 'password']

    captcha.widget.attrs.update({'class': 'form-control', 'autocomplete': "off"})

    password = forms.CharField(max_length=13, required=False)
    username = forms.CharField(max_length=13, required=False)
    confirm_code = forms.IntegerField(required=True)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.username = obj.phone
        if commit:
            obj.save()
        return obj

    def clean(self):
        request = self.initial['request']
        cleaned_data = super(UserForm, self).clean()
        if cleaned_data['confirm_code'] != request.session.get('confirm_code', None):
            raise ValidationError(_('Your SMS Code is wrong!'))
        return cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['customer']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']

    # username = forms.CharField(max_length=13, required=False)

    def save(self, commit=True):
        obj = super(UserUpdateForm, self).save(commit=False)
        obj.username = obj.phone
        if commit:
            obj.save()
        return obj


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['image']
