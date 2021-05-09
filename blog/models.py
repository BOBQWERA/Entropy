from django.db import models

from Entropy.settings import AUTH_USER_MODEL

class Blog(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    headline = models.CharField(max_length=50)
    text = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    hits = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    share = models.BooleanField(default=True)
    abstract = models.CharField(max_length=100,default="暂无简介，进来看看吧")