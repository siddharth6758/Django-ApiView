import random,string,os
from django.db import models
from usersapp.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator

def pk_generator():
    charset = string.ascii_uppercase + string.digits
    return ''.join(random.choices(charset,k=6))

def pk_comment_generator():
    charset = string.ascii_uppercase + string.digits
    return ''.join(random.choices(charset,k=12))

  
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
    course_id = models.CharField(primary_key=True,default=pk_generator)
    details = models.JSONField(default=course_details)
    course_uploaded_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    uploaded_on = models.DateField(auto_now_add=True)
    thumbnail = models.CharField(max_length=300,null=True,blank=True)
    
    def save(self,*args,**kwargs):
        if not self.course_id:
            self.course_id = pk_generator()
        super().save(*args, **kwargs)
        


class Lesson(models.Model):
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    details = models.JSONField(default=lesson_details)
    video = models.CharField(max_length=300,null=True,blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    
    
class Review(models.Model):
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    review_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    review_on = models.DateTimeField(auto_now_add=True)
    review = models.CharField(max_length=200)
    rate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    def save(self,*args,**kwargs):
        super().save(*args, **kwargs)
        course = self.course_id
        ratings = Review.objects.filter(course_id=course)
        total_rate = sum(rating.rate for rating in ratings)
        num_rate = len(ratings)
        if num_rate>0:
            avg_rating = total_rate/num_rate
        else:
            avg_rating = 0
        course.details['avg_rating'] = avg_rating
        course.details['rating_count'] = num_rate
        course.save()
        
        
class Comments(models.Model):
    comment_id = models.CharField(primary_key=True,default=pk_comment_generator)
    comment_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment_on = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100)
    lesson_id = models.ForeignKey(Lesson,on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        if not self.comment_id:
            self.comment_id = pk_comment_generator()
        super().save(*args, **kwargs)


class Reply(models.Model):
    reply_to = models.ForeignKey(Comments,on_delete=models.CASCADE)
    reply_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    reply = models.CharField(max_length=100)
    reply_time = models.DateTimeField(auto_now_add=True)
    

class Enrollment(models.Model):
    course_id = models.ManyToManyField(CustomUser)