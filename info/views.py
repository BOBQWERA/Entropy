from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import HeaderMenu
from .serializers import HeaderMenuSerializer

from user.views import check_permission

class HeaderMenuView(APIView):
    def post(self,request):
        data = request.data
        permiss_code = check_permission(data)
        menus = HeaderMenu.objects.filter(level__contains=str(permiss_code))
        serializer = HeaderMenuSerializer(menus,many=True)
        return Response(serializer.data)

