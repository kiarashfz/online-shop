from django.db import models
from location_field.models.plain import PlainLocationField

from core.models import BaseModel, SingletonBaseModel
from django.utils.translation import gettext_lazy as _


class Question(BaseModel):
    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    question = models.TextField(
        verbose_name=_('Question'),
        help_text=_('This is frequently asked question!')
    )

    answer = models.TextField(
        verbose_name=_('Answer'),
    )


class SiteSetting(SingletonBaseModel):
    site_name = models.CharField(max_length=100)
    location = PlainLocationField(based_fields=['city'], zoom=7)

    def __str__(self):
        return self.site_name
