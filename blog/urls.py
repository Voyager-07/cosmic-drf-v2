from django.urls import path
from .views import *

urlpatterns = [
    path('', CreatePostView.as_view()),
    path('bulk/', PostListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('delete/', DeletePostView.as_view()),
    path('verify/', VerifyPostView.as_view()), 
    path('image-upload/', ImageUploadView.as_view()), 
]
