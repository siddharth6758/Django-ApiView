from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from courseapp.models import *
from courseapp.serializers import *
from usersapp.models import *
import shutil


def save_tbn_vids(data,filename):
    ext = os.path.splitext(filename)[1]
    if ext == 'mp4':
        filename = f'vid_{data}{ext}'
        return os.path.join('lectures',filename)
    elif any(i in ext for i in ['jpg','jpeg','png']):
        filename = f'tbn_{data}{ext}'
        return os.path.join('thumbnails',filename)
    else:
        return f'Wrong file format for {data}...'


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
        dest_path = os.path.join(settings.MEDIA_ROOT,save_tbn_vids(serializer.data['course_id'],tbn_file))
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
            print(media_url)
            tbn_file = None
            for i in os.listdir(media_url):
                if c_id in i:
                    tbn_file = i
            print(tbn_file)
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
    pass


class CommentAPIView(APIView):
    
    def post(self,req,type):
        pass