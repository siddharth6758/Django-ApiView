from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from usersapp.models import *
from usersapp.serializers import *


class UserAuthAPIView(APIView):

    @csrf_exempt
    def post(self, req, type):
        if type == "login":
            email = req.data["email"]
            password = req.data["password"]
            print(email, password)
            if not CustomUser.objects.filter(email=email).exists():
                return Response({"error": f"{email} User does not exists!"})
            else:
                user = authenticate(req, email=email, password=password)
                if user is None:
                    return Response({"error": "Credentials are incorrect!"})
                else:
                    userdata = UserAppSerializer(data=req.data)
                    login(req, user)
                    if not userdata.is_valid():
                        return Response({
                            "error": userdata.errors
                            })
                    return Response(
                        {
                            "success": "User logged in!",
                            "user-data": userdata.data,
                        }
                    )
        if type == "signup":
            serializer = UserAppSerializer(data=req.data)
            if not serializer.is_valid():
                return Response({"error": serializer.errors})
            serializer.save()
            user = CustomUser.objects.get(email=serializer.data['email'])
            token,_ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "success": "User registered!",
                    "user-data": serializer.data,
                    "token": token.key,
                }
            )