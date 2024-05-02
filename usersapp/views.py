from django.contrib.auth import login, logout, authenticate
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from usersapp.models import *
from usersapp.serializers import *


# class LogoutAPIView(APIView):
    
#     def post(self,req):
#         print(req)
#         token,_ = Token.objects.get(user = req.user)
#         print(token,'---deleting')
#         Token.objects.filter(user=req.user).delete()
#         return Response({"message": "User logged out successfully."})     
    
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
                else:
                    token,_ = Token.objects.get_or_create(user=user)
                    # req.header = {
                    #     'Authorization': token.key
                    # }
                    login(req, user)
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
        else:
            return Response({"error": 'Invalid authentication'})
        
    def delete(self, req, type):
        print(req.data)
        if type == "logout":
            if req.user.is_authenticated:
                Token.objects.filter(user=req.user).delete()
                logout(req)
                return Response({"success": "User logged out!"})
            else:
                return Response({"error": "User is not authenticated!"})
