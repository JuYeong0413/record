from django.db import models
from django.utils.translation import ugettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("생성된 시간"), auto_now_add=True)
    updated_at = models.DateTimeField(_("수정된 시간"), auto_now=True)

    class Meta:
        abstract = True