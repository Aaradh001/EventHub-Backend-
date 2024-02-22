from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClientProfileSerializer
from decouple import config
from django.conf import settings
# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        print("Entered RegisterView")
        print(request.data)
        serializer = ClientProfileSerializer(data = request.data)
        print('Client Register Serialized')
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)  

        content ={'Message':'User Registered Successfully'}
        return Response(content,status=status.HTTP_201_CREATED,)