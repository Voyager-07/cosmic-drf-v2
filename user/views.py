from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import SignupSerializer, SigninSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            token = RefreshToken.for_user(user)
            return Response({'jwt': str(token.access_token)}, status=201)
        return Response(serializer.errors, status=400)

class SigninView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                token = RefreshToken.for_user(user)
                return Response({'jwt': str(token.access_token)}, status=200)
            return Response({'msg': 'Invalid credentials'}, status=401)
        return Response(serializer.errors, status=400)
