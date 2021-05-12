from abc import get_cache_token

from django.contrib.auth.models import User
from blog.views import BlogsView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import serializers, status

from user.models import UserProfile,LevelType
from user.views import get_user_id_by_token

from blog.models import Blog
from blog.serializers import BlogSerializer

from forum.models import Posting,Comment
from forum.serializers import PostingSerializer,CommentSerializer

def base_report_function(data,detail):
    rid = data.get('id')
    if not rid:
        return Response({"detail":detail+"为空"},status=status.HTTP_400_BAD_REQUEST)
    user_id = get_user_id_by_token(data)
    if isinstance(user_id,Response):
        return user_id
    user = get_object_or_404(UserProfile,id=user_id)
    return rid

def base_delete_function(data,detail,model):
    did = data.get('id')
    if not did:
        return Response({"detail":detail+"为空"},status=status.HTTP_400_BAD_REQUEST)
    message = get_user_id_by_token(data)
    if isinstance(message,Response):
        return message
    user_id = message
    user = get_object_or_404(UserProfile,id=user_id)
    if user.level not in [LevelType.SUPER_USER,LevelType.ADMIN]:
        return Response({"detail":"您没有权限"},status=status.HTTP_400_BAD_REQUEST)
    item = get_object_or_404(model,id=did)
    item.delete()
    return Response({"detail":"ok"},status=status.HTTP_400_BAD_REQUEST)

class ReportBlogView(APIView):
    def post(self,request):
        data = request.data
        message = base_report_function(data,'博客')
        if isinstance(message,Response):
            return message
        bid = message
        blog = get_object_or_404(Blog,id=bid)
        blog.available = False
        blog.save()
        return Response({"detail":"ok"},status.HTTP_200_OK)

    def delete(self,request):
        data = request.data
        return base_delete_function(data,'博客',Blog)

class ReportPostingView(APIView):
    def post(self,request):
        data = request.data
        message = base_report_function(data,'帖子')
        if isinstance(message,Response):
            return message
        pid = message
        posting = get_object_or_404(Posting,id=pid)
        posting.available = False
        posting.save()
        return Response({"detail":"ok"},status.HTTP_200_OK)

class ReportCommentView(APIView):
    def post(self,request):
        data = request.data
        message = base_report_function(data,'评论')
        if isinstance(message,Response):
            return message
        cid = message
        comment = get_object_or_404(Comment,id=cid)
        comment.available = False
        comment.save()
        return Response({"detail":"ok"},status.HTTP_200_OK)

class DealWithReport(APIView):
    def post(self,request):
        data = request.data
        message = get_user_id_by_token(data)
        if isinstance(message,Response):
            return message
        user = get_object_or_404(UserProfile,id=message)
        if user.level not in [LevelType.SUPER_USER,LevelType.ADMIN]:
            return Response({"detail":"您没有权限"},status=status.HTTP_400_BAD_REQUEST)
        report_blog_list = Blog.objects.filter(available=False)
        report_posting_list = Posting.objects.filter(available=False)
        report_comment_list = Comment.objects.filter(available=False)
        serializer_blog = BlogSerializer(report_blog_list,many=True)
        serializer_posting = PostingSerializer(report_posting_list,many=True)
        serializer_comment = CommentSerializer(report_comment_list,many=True)
        return Response({
            "blog":serializer_blog.data,
            "posting":serializer_posting.data,
            "comment":serializer_comment.data,
        },status=status.HTTP_200_OK)