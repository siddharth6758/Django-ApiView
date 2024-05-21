from django.urls import path
from courseapp.views import *

urlpatterns = [
    path('course', CourseAPIView.as_view(http_method_names=['post','patch','delete']),name='courseapi'),
    path('course/lessons', LessonsAPIView.as_view(http_method_names=['post','patch','delete','get']),name='lessonapi'),
    path('course/<str:type>', CourseAPIView.as_view(http_method_names=['get']),name='courseapi'),
    path('comments/<str:type>', CommentAPIView.as_view(),name='commentapi'),
]
