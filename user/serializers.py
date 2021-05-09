import re

from datetime import datetime,timedelta

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenVerifySerializer
from jwt import decode as jwt_decode
from jwt.exceptions import ExpiredSignatureError

from django.utils import timezone

from .models import  LevelType,GenderType,UserProfile,Apply,RegisterCodeSaver

from Entropy import  settings

def ReTel(tel):
    reg = r"^1[3-9]\d{9}$"
    return bool(re.match(reg, tel))

class GetLevelMethod(object):
    def get_level(self,obj):
        return dict(
            id = obj.level,
            type = LevelType.LEVEL_DESCRIBE[obj.level]
        )



class UserMsgSerializer(serializers.ModelSerializer,GetLevelMethod):
    level = serializers.SerializerMethodField()
    avatar = serializers.CharField(source='avatar.avatar.url', read_only=True, default='/upload/a.png')
    class Meta:
        model = UserProfile
        fields = (
            'id','nickname','avatar','level','score','credit','gender',
        )

class UserDetailSerializer(serializers.ModelSerializer,GetLevelMethod):
    level = serializers.SerializerMethodField()
    avatar = serializers.CharField(source='avatar.avatar.url',read_only=True,default='/upload/a.png')
    friend = UserMsgSerializer(many=True,read_only=True)
    can_sign = serializers.SerializerMethodField()
    apply = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = (
            'id','nickname','username','level','avatar',
            'score','credit','gender','telephone','signature',
            'last_logined','last_signed','friend','can_sign','apply',
        )

    def get_can_sign(self,obj):
        return timezone.now().date() != obj.last_signed.date()

    def get_apply(self,obj):
        data = []
        for apply in Apply.objects.filter(to_user=obj.id):
            data.append({
                "user":apply.from_user.nickname,
                "hello":apply.hello,
                "id":apply.from_user.id,
            })
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserDetailSerializer(self.user).data

        return data


class MyTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        try:
            decoded_data = jwt_decode(attrs['token'], settings.SECRET_KEY, algorithms=["HS256"])

            return {'detail': 'access'}

        except ExpiredSignatureError:
            return {'detail': 'expire'}
        except:
            return {'detail': 'infoError'}