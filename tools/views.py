from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .models import Tools,Files
from .serializers import ToolsSerializer,FilesSerializer

from rest_framework.decorators import action
from django.http import FileResponse

class ToolsView(APIView):
    def get(self,request):
        tools = Tools.objects.all()
        serializer = ToolsSerializer(tools,many=True)
        return Response(serializer.data)

class FileViewSet(ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

class DownloadView(APIView):
    def get(self,request,fid):
        password = request.GET.get('password')
        file = get_object_or_404(Files,id=fid)
        if file.password:
            if not password:
                return Response({"detail":"文件需要密码"},status=status.HTTP_400_BAD_REQUEST)
            elif password != file.password:
                return Response({"detail":"密码错误"},status=status.HTTP_400_BAD_REQUEST)
        response = FileResponse(open(file.file.path, 'rb'))
        return response
