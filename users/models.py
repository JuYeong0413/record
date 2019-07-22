from django.contrib.auth.models import AbstractUser
from share.timestamp import TimeStampedModel
from django.db.models import *
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(AbstractUser, TimeStampedModel):
    followings = ManyToManyField("self", related_name='followers', symmetrical=False)
    image = ImageField(_("프로필사진"), upload_to="profile_img/", default="images/default_profile.jpg")
    introduction = CharField(_("소개"),max_length=200, blank=True)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = "사용자"