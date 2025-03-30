from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer,AuthTokenSerializer
from rest_framework import status


# Create your views here.
class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })
    
class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        print(request.user)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)