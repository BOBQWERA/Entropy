from rest_framework.response import Response
from rest_framework import status
class Message(object):
    @staticmethod
    def response_data(msg,key="detail",status=status.HTTP_404_NOT_FOUND):
        return Response({key:msg},status=status)

    @staticmethod
    def fill_data(pattern, data):
        return pattern % data

class NormalMessage(Message):
    SUCCESS = 'ok'
    AUTHENTICATION_SUCCESS = '校验成功'
    REGISTER_SUCCESS = '注册成功'
    @staticmethod
    def response_data(msg,key="detail",status=status.HTTP_200_OK):
        return Response({key:msg},status=status)


class ErrorMessage(Message):
    NOT_OPERATED_BY_SELF = '非本人操作'
    EXPIRED = '过期'
    AUTHENTICATION_FAILED = '校验失败'
    CANNOT_BE_NONE_OR_EMPTY = '%s不可不填或为空'
    CANNOT_BE_NONE = '%s不可为空'
    HAVE_BEEN_USED = '%s已被使用'
    HAVENOT_BEEN_EXIST = '%s尚未存在'
    CANNOT_HAS_SPACE = '%s不能包含空格'
    NOT_FIT = '%s格式不适合'
    CANNOT_FIT = '%s为非法模式'
    
    @staticmethod
    def response_data(msg,key="detail",status=status.HTTP_400_BAD_REQUEST):
        return Response({key:msg},status=status)