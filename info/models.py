from django.db import models
# Create your models here.

class StatusType:
    BLACKLIST_USER = 0
    HAVE_NOT_LOGINED = 1
    LOGINED = 2
    AUTHENTICATED_USER = 3
    SUPER_USER = 4
    ADMIN = 5
    
    



class HeaderMenu(models.Model):
    name = models.CharField(max_length=10)
    level = models.CharField(default='012345',max_length=10)
    url = models.CharField(max_length=10)
    orderkey = models.IntegerField()

    class Meta:
        ordering = ['orderkey']

    def __str__(self):
        return f'<Menu:{self.name}->{self.url}>'