from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from courseapp.models import *
from courseapp.serializers import *


class CourseAPIView(APIView):
    pass