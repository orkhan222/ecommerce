from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from backend.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

class LoginTokenView(TokenObtainPairView):
    serializer_class = TokenPairSerializers


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


class UserDetail(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        user = User.objects.filter(id=self.request.user.id)
        serializer = UserSerializers(user, many=True)
        return Response(serializer.data)
