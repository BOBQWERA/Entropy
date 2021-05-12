from django.urls import path
from . import views
urlpatterns = [
    path('report/blog',views.ReportBlogView.as_view()),
    path('report/posting',views.ReportPostingView.as_view()),
    path('report/blog',views.ReportCommentView.as_view()),
]
