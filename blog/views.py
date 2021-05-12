from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .models import Blog
from .serializers import BlogSerializer

from user.models import UserProfile
from user.views import get_user_id_by_token,DataChecker

class BlogsView(APIView):
    def get(self,request):
        blogs = Blog.objects.filter(share=True)
        serializer = BlogSerializer(blogs,many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        user_id = data.get('user_id')
        user = get_object_or_404(UserProfile,id=user_id)
        blogs = Blog.objects.filter(author=user,share=True)
        serializer = BlogSerializer(blogs,many=True)
        return Response(serializer.data)

class BlogView(APIView):
    def get(self,request,bid):
        blog = get_object_or_404(Blog,id=bid)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    def post(self,request,bid=None):
        data = request.data
        user_id = data.get('user_id')
        analyse_token = get_user_id_by_token(data)
        if isinstance(analyse_token,Response):
            return analyse_token
        elif user_id != analyse_token:
            return Response({"detail":"非本人操作"},status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(UserProfile,id=user_id)
        headline = data.get('headline')
        abstract = data.get('abstract')
        context = data.get('context')
        check_result = (
            DataChecker.check_None_or_empty(headline,'标题'),
            DataChecker.check_None_or_empty(abstract,'摘要'),
            DataChecker.check_None_or_empty(context,'内容'),
        )
        if (valid_data_or_error:=DataChecker.check_all_right(check_result)) != True:
            return valid_data_or_error
        Blog.objects.create(author=user,headline=headline,text=context,abstract=abstract)
        return Response({"detail":"ok"},status=status.HTTP_200_OK)
        
class FriendBlogView(APIView):
    def post(self,request):
        data = request.data
        user_id = get_user_id_by_token(data)
        if isinstance(user_id,Response):
            return user_id
        user = get_object_or_404(UserProfile,id=user_id)
        friend_blog = []
        friends = user.friend.all()
        for friend in friends:
            blogs = Blog.objects.filter(author=friend)
            for blog in blogs:
                friend_blog.append(blog)
        serializer = BlogSerializer(friend_blog,many=True)
        return Response(serializer.data)
