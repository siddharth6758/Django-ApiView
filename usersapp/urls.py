from django.urls import path
from usersapp.views import *

urlpatterns = [
    path('user-auth/<str:type>', UserAuthAPIView.as_view(),name='userauthapi'),
]
