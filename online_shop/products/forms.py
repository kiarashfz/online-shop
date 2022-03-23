from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from products.models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
