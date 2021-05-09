import base64
from uuid import uuid1

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from Entropy.settings import AUTH_USER_MODEL


def guess_content_type(filename):
    if '.' not in filename:
        return ''
    else:
        guessType = filename.split('.')[-1]
        if len(guessType) > 5 and guessType != 'markdown':
            return ''
        return guessType

def user_directory_path(instance, filename):
    uuidString = str(uuid1())
    base64String = base64.b64encode(
        filename.encode('utf-8')).decode('utf-8')[0:10]
    contentType = guess_content_type(filename)
    if contentType:
        contentType = '.'+contentType
    return uuidString+'-'+base64String+contentType

class LevelType(object):
    BLACKLIST_USER = 0
    ORDINARY_USER = 1
    AUTHENTICATED_USER = 2
    SUPER_USER = 3
    ADMIN = 4

    LEVEL_DESCRIBE = {
        BLACKLIST_USER:'黑名单用户',
        ORDINARY_USER:'普通用户',
        AUTHENTICATED_USER:'认证用户',
        SUPER_USER:'超级用户',
        ADMIN:'管理员'
    }


class GenderType(object):
    MALE = 0
    FEMALE = 1
    OTHER = 2

    GENDER_DESCRIBE = {
        MALE:'男性',
        FEMALE:'女性',
        OTHER:'其他'
    }

class AvatarFiles(models.Model):
    avatar = models.ImageField(upload_to=user_directory_path)

class Apply(models.Model):
    from_user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='from_user')
    to_user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='to_user')
    hello = models.CharField(max_length=100)

class UserProfile(AbstractUser):
    LEVEL_CHOICE = tuple(LevelType.LEVEL_DESCRIBE.items())
    GENDER_CHOICE = tuple(GenderType.GENDER_DESCRIBE.items())
    nickname = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)
    level = models.IntegerField(default=LevelType.ORDINARY_USER,choices=LEVEL_CHOICE)
    gender = models.IntegerField(default=GenderType.OTHER,choices=GENDER_CHOICE)
    credit = models.IntegerField(default=100)
    score = models.IntegerField(default=0)
    avatar = models.OneToOneField('AvatarFiles',null=True,on_delete=models.SET_NULL)
    friend = models.ManyToManyField('self',related_name='friend')
    friend_apply = models.ManyToManyField('self',through=Apply)
    last_logined = models.DateTimeField(auto_now_add=True)
    last_signed = models.DateTimeField(auto_now=True)
    signature = models.CharField(max_length=100,null=True,blank=True)

class RegisterCodeSaver(models.Model):
    telephone = models.CharField(max_length=11)
    smscode = models.CharField(max_length=6)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
