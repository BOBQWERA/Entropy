from django.db import models

from Entropy.settings import AUTH_USER_MODEL

class Section(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Posting(models.Model):
    landlord = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    headline = models.CharField(max_length=30)
    text = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    floor = models.IntegerField(default=1)
    section = models.ForeignKey('Section',on_delete=models.CASCADE)
    class Meta:
        ordering = ['-pub_time']

    def __str__(self):
        return self.headline

class Comment(models.Model):
    publisher = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    posting = models.ForeignKey('Posting',on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    floor = models.IntegerField()
    append_file = models.FileField(upload_to='uploads/',null=True)
    


