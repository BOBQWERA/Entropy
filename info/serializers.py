from rest_framework import serializers

from .models import HeaderMenu

class HeaderMenuSerializer(serializers.ModelSerializer):
    strid = serializers.CharField(source='id')
    class Meta:
        model = HeaderMenu
        fields = [
            'name','strid','url'
        ]