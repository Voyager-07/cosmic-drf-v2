from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import SignupSerializer, SigninSerializer, UserSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import cloudinary.uploader

class UploadProfilePicture(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES.get('image')  # 'file' is the key in form-data

        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = cloudinary.uploader.upload(file_obj)
            url = result.get('secure_url')
            return Response({"url": url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

class UserMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
from rest_framework.generics import RetrieveAPIView
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            user_data = UserSerializer(user).data
            return Response({
                'refresh': str(refresh),
                'access': str(access),
                'user': user_data,
            }, status=201)
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
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                user_data = UserSerializer(user).data
                return Response({
                    'refresh': str(refresh),
                    'access': str(access),
                    'user': user_data,
                }, status=200)
            return Response({'msg': 'Invalid credentials'}, status=401)
        return Response(serializer.errors, status=400)
