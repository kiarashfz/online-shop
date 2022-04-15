from django.core.validators import RegexValidator
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

    logo = models.ImageField(
        null=True,
        blank=True,
        default='w-logo.png',
        verbose_name=_('Logo'),
        help_text=_('please upload an image with 100*100 pixels!')
    )

    contact_phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name=_('Contact Phone'),
        validators=[RegexValidator(
            regex='^0\d{2,3}\d{8}$',
            message=_('please enter a valid phone !')
        )]
    )

    contact_email = models.EmailField(
        verbose_name=_('Contact Email'),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('site description'),
        help_text=_('The description wii be show on footer!'),
    )

    email_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('email description'),
        help_text=_('The description wii be show on footer under the email!'),
    )

    telegram_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('telegram link'),
    )

    instagram_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('instagram link'),
    )

    github_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('github link'),
    )

    def __str__(self):
        return self.site_name
