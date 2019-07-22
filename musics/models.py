from django.db import models
from share.timestamp import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from users.models import User

# Create your models here.
class Music(TimeStampedModel):

    writer = models.ForeignKey(User, verbose_name=_('작성자'), on_delete=models.CASCADE)
    title = models.CharField(_('글제목'), max_length=200)
    genre = models.CharField(_('장르'), max_length=200)
    singer = models.CharField(_('가수'), max_length=200)
    lyrics = models.TextField(_('가사'), blank=True)
    link = models.TextField(_('링크'), blank=True)

    class Meta:
        verbose_name = '노래'
        verbose_name_plural = "노래"