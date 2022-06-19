from django.urls import path
from .views import TestView, NewURLView, ListURLView

urlpatterns = [

    path('test', TestView.as_view(), name="test"),
    path('monitor/new_url', NewURLView.as_view(), name="new_url"),
    path('monitor/list_url', ListURLView.as_view(), name="list_urls"),

] 