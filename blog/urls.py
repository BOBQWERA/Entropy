from django.urls import path

from . import views

urlpatterns = [
    path('blog',views.BlogsView.as_view()),
    path('blog/<int:bid>',views.BlogView.as_view()),
    path('blog/friend',views.FriendBlogView.as_view()),
]
