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
    elif ext in ['jpg','jpeg','png']:
        filename = f'tbn_{data}{ext}'
        return os.path.join('thumbnails',filename)
    else:
        return 'Wrong file format...'


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
        
        
    def post(self,req,type):
        if type == 'upload':
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
        else:
            return Response({"error": 'Invalid url authentication'})
            
    

class CommentAPIView(APIView):
    
    def post(self,req,type):
        pass