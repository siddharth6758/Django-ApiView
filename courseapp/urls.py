from django.urls import path
from courseapp.views import *

urlpatterns = [
    path('course/<str:type>', CourseAPIView.as_view(),name='courseapi'),
]
