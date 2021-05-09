from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'files', views.FileViewSet)

urlpatterns = [
    path("tools/", views.ToolsView.as_view()),
    path("download/<int:fid>",views.DownloadView.as_view()),
    path('', include(router.urls)),
]