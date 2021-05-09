from rest_framework import serializers

from .models import *

from user.serializers import UserMsgSerializer

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"

class PostingSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    landlord = UserMsgSerializer()
    section = SectionSerializer()
    pub_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Posting
        fields = "__all__"
    def get_text(self,obj):
        if len(obj.text)>60:
            return obj.text[:60]+'...'
        return obj.text

class CommentSerializer(serializers.ModelSerializer):
    publisher = UserMsgSerializer()
    posting = PostingSerializer()
    pub_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Comment
        fields = "__all__"

