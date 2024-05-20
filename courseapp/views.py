from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from courseapp.models import *
from courseapp.serializers import *
from usersapp.models import *

class CourseAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    # parser_classes = [MultiPartParser, FormParser]

    def post(self,req,type):
        if type == 'upload':
            if req.session.get('user_id',None):
                user = CustomUser.objects.get(email=req.session.get('user_id',None))
                req.data['course_uploaded_by'] = user.id
            else:
                return Response({
                    'error':'User not logged in!'
                })
            if req.data['thumbnail']:
                print(req.data['thumbnail'])
                path = req.data['thumbnail']
                data = open(path,'rb')
                print(data)
            else:
                return Response({
                    'error':'Thumbnail path not provided!'
                })
            serializer = CourseSerializer(data=req.data)
            if not serializer.is_valid():
                return Response({
                    'error':serializer.errors
                })
            serializer.save()
            return Response({
                'success':'Course created!',
                'data':serializer.data
            })
        else:
            return Response({"error": 'Invalid url authentication'})
            
    

class CommentAPIView(APIView):
    
    def post(self,req,type):
        pass