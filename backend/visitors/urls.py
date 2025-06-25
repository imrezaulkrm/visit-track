from django.urls import path
from .views import visitor_stats, track_visitor

app_name = "visitors"

urlpatterns = [
    path('stats/', visitor_stats, name='visitor_stats'),
    path('track/', track_visitor, name='track_visitor'),
]
