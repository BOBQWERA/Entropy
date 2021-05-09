from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view()),  # 登录
    path('refreshtoken', views.MyTokenRefreshView.as_view()),  # 刷新token
    path('info', views.MyTokenVerifyView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('userinfo',views.UserMsgView.as_view()),
    path('addfriend',views.AddFriendView.as_view()),
    path('successfriend',views.SuccessFriendView.as_view()),
]