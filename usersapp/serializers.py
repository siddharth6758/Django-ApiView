from rest_framework import serializers
from usersapp.models import *

class UserAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def create(self,data):
        user = CustomUser.objects.create(
            email = data['email'],
            username = data['username'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            address = data['address'],
            phone = data['phone']
        )
        user.set_password(data['password'])
        user.save()
        return user