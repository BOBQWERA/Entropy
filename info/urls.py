from django.urls import path
from . import views

urlpatterns = [
    path('headermenu',views.HeaderMenuView.as_view())
]