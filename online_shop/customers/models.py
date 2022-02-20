from django.db import models
from core.models import BaseModel, User
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Address(BaseModel):
    class Meta:
        verbose_name = _('Address')

    PROVINCES = [
        ('thr', _('Tehran')),
        ('az-sh', _('Azarbayejan Sharghi')),
        ('az-gh', _('Azarbayejan Gharbi')),
        ('ard', _('Ardebil')),
        ('esf', _('Esfehan')),
        ('alb', _('Alborz')),
        ('ilm', _('Ilam')),
        ('bsh', _('Booshehr')),
        ('chm', _('Charmahal o Bakhtiari')),
        ('kh-j', _('Khorasan Jonobi')),
        ('kh-r', _('Khorasan Razavi')),
        ('kh-sh', _('Khorasan Shomali')),
        ('khz', _('Khoozestan')),
        ('znj', _('Zanjan')),
        ('smn', _('Semnan')),
        ('sbch', _('Sistan Baloochestan')),
        ('frs', _('Fars')),
        ('ghz', _('Ghazvin')),
        ('qom', _('Qom')),
        ('krd', _('Kordestan')),
        ('krm', _('Kerman')),
        ('kr-sh', _('Kerman Shah')),
        ('khb', _('Kohkilooye Boyer Ahmad')),
        ('gls', _('Golestan')),
        ('gil', _('Gilan')),
        ('lor', _('Lorestan')),
        ('maz', _('Mazandaran')),
        ('mrk', _('Markazi')),
        ('hrm', _('Hormozgan')),
        ('hmd', _('Hamedan')),
        ('yzd', _('Yazd')),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
        verbose_name=_('Customer'),
        help_text=_('Customer of this address!'),
    )

    province = models.CharField(
        max_length=7,
        choices=PROVINCES,
        verbose_name=_('Province'),
    )

    city = models.CharField(
        max_length=31,
        verbose_name=_('City'),
    )

    area = models.CharField(
        max_length=31,
        verbose_name=_('Area'),
    )

    avenue = models.CharField(
        max_length=31,
        verbose_name=_('Avenue'),
    )

    street = models.CharField(
        max_length=31,
        null=True,
        blank=True,
        verbose_name=_('Street'),
    )

    alley = models.CharField(
        max_length=31,
        null=True,
        blank=True,
        verbose_name=_('Alley'),
    )

    no = models.PositiveSmallIntegerField(
        verbose_name=_('No.'),
    )

    unit = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Unit'),
    )

    floor = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Floor'),
    )

    postal_code = models.CharField(
        max_length=31,
        verbose_name=_('Postal Code'),
    )
