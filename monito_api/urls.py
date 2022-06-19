from django.urls import path
from .views import TestView, NewURLView

urlpatterns = [

    path('test', TestView.as_view(), name="test"),
    path('monitor/new_url', NewURLView.as_view(), name="new_url"),

] 