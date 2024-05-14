from rest_framework import serializers
from courseapp.models import *
from usersapp.serializers import *
class CourseSerializer(serializers.ModelSerializer):
    course_uploaded_by = UserAppSerializer()
    class Meta:
        model = Course
        fields = "__all__"
        
class LessonSerializer(serializers.ModelSerializer):
    course_id = CourseSerializer()
    class Meta:
        model = Lesson
        fields = "__all__"
        
class CommentsSerializer(serializers.ModelSerializer):
    comment_by = UserAppSerializer()
    lesson_id = LessonSerializer()
    class Meta:
        model = Comments
        fields = "__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    course_id = CourseSerializer()
    review_by = UserAppSerializer()
    class Meta:
        model = Review
        fields = "__all__"