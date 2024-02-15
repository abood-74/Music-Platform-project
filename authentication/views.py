from rest_framework.views import  APIView
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from users.serializers import *
from knox.auth import TokenAuthentication
from rest_framework.status import *


class RegisterAPI(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            return Response(data={
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response(data={
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
