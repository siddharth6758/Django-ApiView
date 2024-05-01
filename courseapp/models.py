from django.db import models
from usersapp.models import CustomUser
import random,string,os

def pk_generator():
    charset = string.ascii_uppercase + string.digits
    return ''.join(random.choices(charset,k=6))


def save_tbn_vids(self,filename):
    ext = os.path.splitext(filename)[1]
    if ext == 'mp4':
        filename = f'vid_{self.course_id}.{ext}'
        return os.path.join('lectures',filename)
    else:
        filename = f'tbn_{self.course_id}.{ext}'
        return os.path.join('thumbnails',filename)
    

def course_details():
    return {
        'title':'',
        'description':'',
        'domain':'',
        'price':0,
        'avg_rating':0,
        'rating_count':0
    }


def lesson_details():
    return {
        'title':'',
        'description':''
    }

class Course(models.Model):
    course_id = models.CharField(primary_key=True)
    details = models.JSONField(default=course_details)
    course_uploaded_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    uploaded_on = models.DateField(auto_now_add=True)
    thumbnail = models.FileField(upload_to=save_tbn_vids)
    
    def save(self,*args,**kwargs):
        if not self.prod_id:
            self.prod_id = pk_generator()
        super().save(*args, **kwargs)
        


class Lesson(models.Model):
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    details = models.JSONField(default=lesson_details)
    video = models.FileField(upload_to=save_tbn_vids)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    
class Review(models.Model):
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    review_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    review_on = models.DateTimeField(auto_now_add=True)
    review = models.CharField(max_length=200)