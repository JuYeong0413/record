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
    description = models.TextField(_('설명'), blank=True)
    tags = TaggableManager(blank=True)
    liked_users = models.ManyToManyField(User, blank=True, related_name="liked_users", through='Like')
    cover = models.ImageField(_('커버이미지'), null=True, upload_to="playlist_cover/",  default="images/default_cover.png")
    title = models.CharField(_('제목'), max_length=200)

    def comments(self):
        return Comment.objects.filter(playlist=self)
    
    @property
    def comments_count(self):
        comments = Comment.objects.filter(playlist=self)
        return comments.count()

    class Meta:
        verbose_name = '플레이리스트'
        verbose_name_plural = "플레이리스트"

    @property
    def likes_count(self):
        return self.liked_users.count()


class Comment(TimeStampedModel):
    playlist = models.ForeignKey(Playlist, verbose_name=_('플레이리스트'), on_delete=models.CASCADE)
    writer = models.ForeignKey(User, verbose_name=_('작성자'), on_delete=models.CASCADE)
    message = models.TextField(_('내용'))

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = "댓글"

class Like(TimeStampedModel):
    creator = models.ForeignKey(User, verbose_name=_('작성자'), on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, verbose_name=_('플레이리스트'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'
        unique_together = (
            ('creator', 'playlist')
        )