from django.db import models
from django.utils import timezone
from .manager import BaseManager


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Deleted Datetime"),
        help_text=_("This is deleted datetime")
    )

    is_deleted = models.BooleanField(
        default=False,
        editable=False,
        db_index=True,
        verbose_name=_("Deleted status"),
        help_text=_("This is deleted status"),
    )

    is_active = models.BooleanField(
        default=True,
        editable=False,
        verbose_name=_("Active status"),
        help_text=_("This is active status"),
    )

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save(using=using)

    def restore(self):
        self.is_deleted = False
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    # todo: unique error -> restore
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
