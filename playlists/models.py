from django.db import models
from taggit.managers import TaggableManager
from share.timestamp import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from users.models import User
from musics.models import Music

# Create your models here.
class Playlist(TimeStampedModel):

    PLAYLIST_KIND_CHOICES = [
        (0, "public"),
        (1, "private")
    ]

    creator = models.ForeignKey(User, verbose_name=_('생성자'), on_delete=models.CASCADE)
    musics = models.ManyToManyField(Music, verbose_name=_('노래'))
    kinds = models.PositiveSmallIntegerField(_('종류'), choices=PLAYLIST_KIND_CHOICES)
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, verbose_name=_('좋아요'), related_name="liked_users")
    cover = models.ImageField(_('커버이미지'), null=True, upload_to="playlist_cover/",  default="images/default_cover.jpg")
    title = models.CharField(_('제목'), max_length=200)

    class Meta:
        verbose_name = '플레이리스트'
        verbose_name_plural = "플레이리스트"


class Comment(TimeStampedModel):
    playlist = models.ForeignKey(Playlist, verbose_name=_('플레이리스트'), on_delete=models.CASCADE)
    writer = models.ForeignKey(User, verbose_name=_('작성자'), on_delete=models.CASCADE)
    message = models.TextField(_('내용'))

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = "댓글"