from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Customer(BaseModel):
    pass


class Address(BaseModel):
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
    )

    province = models.CharField(
        max_length=7,
        choices=PROVINCES,
    )

    city = models.CharField(
        max_length=31,
    )

    area = models.CharField(
        max_length=31,
    )

    avenue = models.CharField(
        max_length=31,
    )

    street = models.CharField(
        max_length=31,
        null=True,
        blank=True,
    )

    alley = models.CharField(
        max_length=31,
        null=True,
        blank=True,
    )

    no = models.PositiveSmallIntegerField()

    unit = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    floor = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=31,
    )
