from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer, CreatePostSerializer

class CreatePostView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, readtime=5)

class PostListView(generics.ListAPIView):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer

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


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Post.objects.select_related('author').order_by('-created_at')
        return Post.objects.select_related('author').filter(verified=True).order_by('-created_at')


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
