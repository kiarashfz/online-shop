from django.db import models

from core.models import BaseModel
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
