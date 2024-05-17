from django.contrib import admin
from courseapp.models import *
# Register your models here.
admin.site.register(Course)
admin.site.register(Comments)
admin.site.register(Lesson)
admin.site.register(Review)
admin.site.register(Enrollment)