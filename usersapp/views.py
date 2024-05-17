from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from usersapp.models import *
from usersapp.serializers import *

class UserAuthAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def post(self, req, type):
        if type == "login":
            email = req.data["email"]
            password = req.data["password"]
            if not CustomUser.objects.filter(email=email).exists():
                return Response({"error": f"{email} User does not exists!"})
            else:
                user = authenticate(req, email=email, password=password)
                if user is None:
                    return Response({"error": "Credentials are incorrect!"})
                elif user.is_logged_in == True:
                    return Response(
                        {
                            "success": f"{user.username} already logged in!"
                        }
                    )
                else:
                    token,_ = Token.objects.get_or_create(user=user)
                    req.header = {
                        'Authorization': token.key
                    }
                    login(req, user)
                    user.is_logged_in = True
                    user.save()
                    return Response(
                        {
                            "success": "User logged in!",
                            "user-data": req.data,
                            "token":token.key
                        }
                    )
        elif type == "signup":
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
        elif type == "logout":
            user = CustomUser.objects.filter(email=req.data['email']).first()
            if user.is_logged_in == True:
                user.is_logged_in = False
                user.save()
                logout(req)
                return Response({
                    'data':f'{user.email} logged out successfully!'
                })
            else:
                return Response({
                    'data':'User not logged in!'
                })
        else:
            return Response({"error": 'Invalid authentication'})