from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .models import *
from .serializers import *

from user.models import UserProfile
from user.views import DataChecker,get_user_id_by_token,authenticate_self

class SectionView(APIView):
    def get(self,request):
        sid = request.GET.get('sid')
        if sid:
            section = get_object_or_404(Section,id=sid)
            serializer = SectionSerializer(section)
        else:
            sections = Section.objects.all()
            serializer = SectionSerializer(sections,many=True)
        return Response(serializer.data)

class PostingView(APIView):
    def get(self,request):
        sid = request.GET.get('sid')
        pid = request.GET.get('pid')
        if pid:
            posting = get_object_or_404(Posting,id=pid)
            serializer = PostingSerializer(posting)
        elif sid:
            section = get_object_or_404(Section,id=sid)
            postings = Posting.objects.filter(section=section)
            serializer = PostingSerializer(postings,many=True)
        else:
            postings = Posting.objects.all()[:50]
            serializer = PostingSerializer(postings,many=True)
        return Response(serializer.data)
    def post(self,request):
        data = request.data
        print(data)
        user_id = data.get('user_id')
        sid=data.get('sid')
        section = get_object_or_404(Section,id=sid)
        analyse_token = get_user_id_by_token(data)
        if isinstance(analyse_token,Response):
            return analyse_token
        elif user_id != analyse_token:
            return Response({"detail":"非本人操作"},status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(UserProfile,id=user_id)
        check_result = (
            DataChecker.check_None_or_empty(headline:=data.get('headline'),'标题'),
            DataChecker.check_None_or_empty(text:=data.get('text'),'内容'),
        )
        if (valid_data_or_error:=DataChecker.check_all_right(check_result)) != True:
            return valid_data_or_error
        Posting.objects.create(landlord=user,headline=headline,text=text,section = section)
        return Response({"detail":"ok"},status=status.HTTP_200_OK)



class CommentView(APIView):
    def get(self,request):
        pid = request.GET.get('pid')
        posting = get_object_or_404(Posting,id=pid)
        comments = Comment.objects.filter(posting=posting)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)
    def post(self,request):
        data = request.data
        user_id = data.get('user_id')
        pid=data.get('pid')
        posting = get_object_or_404(Posting,id=pid)
        analyse_token = get_user_id_by_token(data)
        if isinstance(analyse_token,Response):
            return analyse_token
        elif user_id != analyse_token:
            return Response({"detail":"非本人操作"},status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(UserProfile,id=user_id)
        check_result = (
            DataChecker.check_None_or_empty(content:=data.get('content'),'内容'),
        )
        if (valid_data_or_error:=DataChecker.check_all_right(check_result)) != True:
            return valid_data_or_error
        floor = posting.floor+1
        posting.floor+=1
        posting.save()
        Comment.objects.create(publisher=user,posting=posting,floor=floor,content=content)
        return Response({"detail":"ok"},status=status.HTTP_200_OK)