from django.urls import path
from .views import TestView, NewURLView, ListURLView, GetURLDetailsView, CurrentURLView, StatisticsView, checkSecurityView

urlpatterns = [

    path('test', TestView.as_view(), name="test"),
    path('monitor/new_url', NewURLView.as_view(), name="new_url"),
    path('monitor/list_url', ListURLView.as_view(), name="list_urls"),
    path('monitor/url_details/<int:url_id>', GetURLDetailsView.as_view(), name="url_details"),
    path('monitor/execute/<int:url_id>', CurrentURLView.as_view(), name="execute_once"),
    path('monitor/stats/<int:url_id>', StatisticsView.as_view(), name="stats"),
    path('monitor/checksecurity', checkSecurityView.as_view(), name='checksecurity')
] 