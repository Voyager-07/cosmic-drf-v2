from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer, CreatePostSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import cloudinary.uploader

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')  # 'file' is the key in form-data

        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = cloudinary.uploader.upload(file_obj)
            url = result.get('secure_url')
            return Response({"url": url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreatePostView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, readtime=5)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]  

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and hasattr(user, 'role') and user.role == 'ADMIN':
            return Post.objects.select_related('author').order_by('-created_at')

        return Post.objects.select_related('author').filter(verified=True).order_by('-created_at')

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'

class DeletePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('id')
        try:
            post = Post.objects.get(pk=post_id, author=request.user)
            post.delete()
            return Response({'msg': 'Deleted'})
        except Post.DoesNotExist:
            return Response({'msg': 'Not found'}, status=404)

from rest_framework.permissions import IsAdminUser
from rest_framework import status

class VerifyPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != 'ADMIN':
            return Response({'msg': 'Unauthorized'}, status=403)

        post_id = request.data.get('id')
        try:
            post = Post.objects.get(pk=post_id)
            post.verified = True
            post.save()
            return Response({'msg': 'Post verified'})
        except Post.DoesNotExist:
            return Response({'msg': 'Post not found'}, status=404)
