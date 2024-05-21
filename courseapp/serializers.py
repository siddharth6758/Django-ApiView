from rest_framework import serializers
from courseapp.models import *
from usersapp.serializers import *
class CourseSerializer(serializers.ModelSerializer):
    course_uploaded_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = Course
        fields = "__all__"
        depth = 1
        
class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Lesson
        fields = "__all__"
        
class CommentsSerializer(serializers.ModelSerializer):
    comment_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    class Meta:
        model = Comments
        fields = "__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    review_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = Review
        fields = "__all__"
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"