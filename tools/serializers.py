from rest_framework import serializers
from .models import Tools,Files

class ToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = "__all__"

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'