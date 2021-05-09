from rest_framework import serializers

from .models import Blog

from user.serializers import UserMsgSerializer

class BlogSerializer(serializers.ModelSerializer):
    author = UserMsgSerializer()
    pub_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Blog
        fields = '__all__'