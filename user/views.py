import re

from rest_framework import mixins,viewsets,status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from jwt.exceptions import ExpiredSignatureError

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from jwt import decode as jwt_decode

from .serializers import UserMsgSerializer,UserDetailSerializer,MyTokenVerifySerializer,MyTokenObtainPairSerializer
from .models import  LevelType,GenderType,UserProfile,RegisterCodeSaver,Apply
from .message import  NormalMessage,ErrorMessage
from .config import GENTER_TYPE

from info.models import StatusType

from Entropy import settings


def ReTel(tel):
    reg = r"^1[3-9]\d{9}$"
    return bool(re.match(reg, tel))

def xor(a,b):
    return a and not b or not a and b

class DataChecker:
    @staticmethod
    def check_all_right(results):
        for res in results:
            if res!=True:
                return Response({'detail': res}, status=status.HTTP_400_BAD_REQUEST)
        return True

    @staticmethod
    def check_None_or_empty(item, detail):
        err_msg = ErrorMessage.CANNOT_BE_NONE_OR_EMPTY
        if ( item is None or len(str(item))) == 0:
            return ErrorMessage.fill_data(err_msg,detail)
        return True

    @staticmethod
    def check_None(item, detail):
        err_msg = ErrorMessage.CANNOT_BE_NONE
        if item is None:
            return ErrorMessage.fill_data(err_msg,detail)
        return True

    @staticmethod
    def check_has_data(model,detail,ex,**kwargs):#except:期望，期望是否存在模型实例
        err_msg_ex_true = ErrorMessage.HAVENOT_BEEN_EXIST
        err_msg_ex_false = ErrorMessage.HAVE_BEEN_USED
        data = model.objects.filter(**kwargs)
        if not xor(data,ex):
            return True
        elif ex:
            return ErrorMessage.fill_data(err_msg_ex_true,detail)
        else:
            return ErrorMessage.fill_data(err_msg_ex_false,detail)

    @staticmethod
    def check_has_space(string,detail):
        err_msg = ErrorMessage.CANNOT_HAS_SPACE
        if ' ' in string:
            return ErrorMessage.fill_data(err_msg,detail)
        return True

    @staticmethod
    def check_true(item,detail,ex=True):
        if not xor(item,ex):
            return True
        return detail

    @staticmethod
    def check_fit(item,match_func,detail,ex=True):
        err_msg_ex_true = ErrorMessage.NOT_FIT
        err_msg_ex_false = ErrorMessage.CANNOT_FIT
        m=match_func(item)
        if not xor(m,ex):
            return True
        elif ex:
            return ErrorMessage.fill_data(err_msg_ex_true,detail)
        else:
            return ErrorMessage.fill_data(err_msg_ex_false,detail)

def get_user_id_by_token(data):
    token = data.get('token')
    print(token)
    error = None
    try:
        token_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        error = ErrorMessage.EXPIRED
    except Exception as e:
        print(e)
        error = ErrorMessage.AUTHENTICATION_FAILED
    if error!=None:
        return Response({'detail':error},status=status.HTTP_400_BAD_REQUEST)
    user_id = token_data.get('user_id')
    return user_id

def check_permission(data):
    auth_res = get_user_id_by_token(data)
    if not isinstance(auth_res, Response):
        user = get_user_by_user_id(auth_res)
        if user != None:
            if user.level == 0:
                return StatusType.BLACKLIST_USER
            elif user.level == 2:
                return StatusType.AUTHENTICATED_USER
            elif user.level == 3:
                return StatusType.SUPER_USER
            elif user.level == 4:
                return StatusType.ADMIN
    return StatusType.HAVE_NOT_LOGINED

def get_user_by_user_id(user_id):
    if not user_id.isdigit():
        return None
    res = UserProfile.objects.filter(id=user_id)
    if res.count() == 0:
        return None
    return res[0]

def authenticate_self(data):
    token_user_id = get_user_id_by_token(data)
    if isinstance(token_user_id,Response):
        return token_user_id
    return data.get('user_id') == token_user_id

def isFriend(this_id,that_id):
    this = get_object_or_404(UserProfile,id=this_id)
    that = get_object_or_404(UserProfile,id=that_id)
    if that in this.friend.all():
        return True
    return False

def hasApply(this_id,that_id):
    for apply in Apply.objects.filter(from_user_id=this_id):
        if str(apply.to_user.id) == str(that_id):
            return True
    return False



class UsernameOrPhonenumBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(username)
            user = UserProfile.objects.get(
                Q(username=username) | Q(telphone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#登录
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#刷新令牌
class MyTokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshSerializer

#验证令牌
class MyTokenVerifyView(TokenViewBase):
    serializer_class = MyTokenVerifySerializer

class UserMsgView(APIView):
    def post(self,request):
        data = request.data
        print(data)
        user_id = data.get('user_id')
        if auth_res:=authenticate_self(data)==True:
            user = get_object_or_404(UserProfile,id=user_id)
            serializer = UserDetailSerializer(user)
            data = serializer.data
        elif auth_res==False:
            user = get_object_or_404(UserProfile,id=user_id)
            serializer = UserMsgSerializer(user)
            self_id = get_user_id_by_token(data)
            data = serializer.data
            is_friend = isFriend(self_id,user_id)
            if not isinstance(is_friend,bool):
                return is_friend
            data['is_friend'] = is_friend
            has_apply = hasApply(self_id,user_id)
            data['has_apply'] = has_apply
        else:
            return auth_res
        return Response(data)


class RegisterView(APIView):
    def post(self,request):
        data = request.data
        check_result = (
            DataChecker.check_None_or_empty(username:=data.get('username'),'用户名'),
            DataChecker.check_None_or_empty(telephone:=data.get('telephone'),'电话号'),
            DataChecker.check_None_or_empty(nickname:=data.get('nickname'),'昵称'),
            DataChecker.check_None_or_empty(password:=data.get('password'),'密码'),
            DataChecker.check_None_or_empty(gender:=GENTER_TYPE.get(data.get('gender')),'性别'),
            DataChecker.check_has_space(password,'密码'),
            DataChecker.check_fit(telephone,ReTel,'电话号'),
            DataChecker.check_has_data(UserProfile,'用户名',False,username=username),
            DataChecker.check_has_data(UserProfile,'电话号',False,telephone=telephone),
        )
        if (valid_data_or_error:=DataChecker.check_all_right(check_result)) != True:
            return valid_data_or_error
        UserProfile.objects.create_user(
            username=username,
            password=password,
            nickname=nickname,
            telephone=telephone,
            gender=gender,
        )
        msg = NormalMessage.REGISTER_SUCCESS
        return NormalMessage.response_data(msg)

class AddFriendView(APIView):
    def post(self,request):
        data = request.data
        user_id = data.get('user_id')
        hello = data.get('hello')
        self_id = get_user_id_by_token(data)
        this = get_object_or_404(UserProfile,id=self_id)
        that = get_object_or_404(UserProfile,id=user_id)
        if Apply.objects.filter(from_user=this,to_user=that).count():
            return Response({"detail":"你已经申请过啦"},status=status.HTTP_400_BAD_REQUEST)
        elif Apply.objects.filter(from_user=that,to_user=this).count():
            return Response({"detail":"对方向你发出了申请，快去查收！"},status=status.HTTP_400_BAD_REQUEST)
        elif isFriend(user_id,self_id):
            return Response({"detail":"你们已经是朋友了！"},status=status.HTTP_400_BAD_REQUEST)
        if not hello:
            hello = f"你好，我是{this.nickname}"
        Apply.objects.create(from_user=this,to_user=that,hello=hello)
        return Response({"detail":"ok"},status=status.HTTP_200_OK)


class SignView(APIView):
    def post(self,request):
        data = request.data
        user_id = get_user_id_by_token(data)
        if isinstance(user_id,Response):
            return user_id
        user = get_object_or_404(UserProfile,id=user_id)
        user.score+=3
        user.save()
        return Response({"detail":"ok"},status=status.HTTP_200_OK)


class SuccessFriendView(APIView):
    def post(self,request):
        data = request.data
        state = data.get("status")
        user_id = get_user_id_by_token(data)
        user = get_object_or_404(UserProfile,id=user_id)
        that_id = data.get("user_id")
        that = get_object_or_404(UserProfile,id=that_id)
        apply = get_object_or_404(Apply,from_user=that,to_user=user)
        if state=="add":
            user.friend.add(that)
            apply.delete()
        elif state=="no":
            apply.delete()
        else:
            return Response({"detail":"非法参数"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"ok"},status=status.HTTP_200_OK)




