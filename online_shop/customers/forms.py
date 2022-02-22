from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'password']

    confirm_password = forms.CharField(max_length=63, required=True, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError(_('Passwords Doesn\'t Match!'))

