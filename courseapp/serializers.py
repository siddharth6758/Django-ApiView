from rest_framework import serializers
from courseapp.models import *
from usersapp.serializers import *
class CourseSerializer(serializers.ModelSerializer):
    course_uploaded_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='course_uploaded_by.email')
    thumbnail = serializers.FileField()
    class Meta:
        model = Course
        fields = "__all__"
        
class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course_id.course_id')
    video = serializers.FileField()
    class Meta:
        model = Lesson
        fields = "__all__"
        
class CommentsSerializer(serializers.ModelSerializer):
    comment_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='comment_by.email')
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), source='lesson_id.id')
    class Meta:
        model = Comments
        fields = "__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course_id.course_id')
    review_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='review_by.email')
    class Meta:
        model = Review
        fields = "__all__"
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"