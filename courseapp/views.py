from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from courseapp.models import *
from courseapp.serializers import *
from usersapp.models import *
import shutil


def save_tbn(data,filename):
    ext = os.path.splitext(filename)[1]
    if any(i in ext for i in ['jpg','jpeg','png']):
        filename = f'tbn_{data}{ext}'
        return os.path.join('thumbnails',filename)
    else:
        return f'Wrong file format for {data}...'
    
    
def save_vids(cid,title,filename):
    ext = os.path.splitext(filename)[1]
    if ext == '.mp4':
        filename = f'vid_{cid}_{title.replace(" ","_")}{ext}'
        if os.path.exists(os.path.join(settings.MEDIA_ROOT,'lectures',cid)):
            return os.path.join('lectures',cid,filename)
        else:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'lectures', cid))
            return os.path.join('lectures',cid,filename)
    else:
        return f'Wrong file format for {cid}_{title}...'


class CourseAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self,req,type):
        if type == 'mycourses':
            courses = Course.objects.filter(course_uploaded_by=req.session['user_id'])
            serializer = CourseSerializer(courses,many=True)
            return Response({
                'data':serializer.data
            })
        elif type == 'showall':
            courses = Course.objects.all()
            serializer = CourseSerializer(courses,many=True)
            return Response({
                'data':serializer.data
            })
        else:
            return Response({"error": 'Invalid url authentication'})
        
        
    def post(self,req):
        if req.session.get('user_id',None):
            user = CustomUser.objects.get(id=req.session.get('user_id',None))
            req.data['course_uploaded_by'] = user.id
        else:
            return Response({
                'error':'User not logged in!'
            })
        serializer = CourseSerializer(data=req.data)
        if not serializer.is_valid():
            return Response({
                'error':serializer.errors
            })
        serializer.save()
        tbn_file = serializer.data['thumbnail']
        dest_path = os.path.join(settings.MEDIA_ROOT,save_tbn(serializer.data['course_id'],tbn_file))
        shutil.copy(tbn_file,dest_path)
        return Response({
            'success':'Course created!',
            'data':serializer.data
        })
        
        
    def patch(self,req):
        try:
            c_id = req.data['course_id']
            course = Course.objects.get(course_id=c_id)
            serializer = CourseSerializer(course,data=req.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success':f'{c_id} updated successfully!',
                    'data':serializer.data
                })
        except Exception as e:
            return Response({
                'error': str(e)
            })
            
            
    def delete(self,req):
        try:
            c_id = req.data['course_id']
            media_url = os.path.join(settings.MEDIA_ROOT,'thumbnails')
            tbn_file = None
            for i in os.listdir(media_url):
                if c_id in i:
                    tbn_file = i
            if tbn_file is not None:
                tbn_path = os.path.join(media_url,tbn_file)
                os.remove(tbn_path)
            else:
                return Response({
                        'error':f'{tbn_file} not found!',
                        'path':f'{tbn_path}'
                    })
            Course.objects.get(course_id=c_id).delete()
            return Response({
                    'success':f'{c_id} deleted successfully!'
                })
        except Exception as e:
            return Response({
                'error': str(e)
            })
    
class LessonsAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    
    def get(self,req):
        if Course.objects.filter(course_id=req.data['course_id']).exists():
            lessons = Lesson.objects.filter(course_id=req.data['course_id'])
            serializer = LessonSerializer(lessons,many=True)
            return Response({
                'data':serializer.data
            })
        else:
            return Response({
                'error':f'{req.data["course_id"]} not found!'
            })


    def post(self,req):
        if req.session.get('user_id',None):
            course = Course.objects.get(course_id=req.data['course_id'])
            if req.session.get('user_id',None) == course.course_uploaded_by.id:
                serializer = LessonSerializer(data=req.data)
                if not serializer.is_valid():
                    return Response({
                        'error':serializer.errors
                    })
                serializer.save()
                video = serializer.data['video']
                dest_path = os.path.join(settings.MEDIA_ROOT,save_vids(serializer.data['course_id'],serializer.data['details']['title'],video))
                shutil.copy(video,dest_path)
                return Response({
                    'success':'Lesson uploaded successfully',
                    'data':serializer.data
                })
            else:
                return Response({
                    'error':'User cannot upload, invalid course creator!'
                })
        else:
            return Response({
                'error':'User not logged in!'
            })
    


class CommentAPIView(APIView):
    pass