from django.urls import path
from .views import SignupView, SigninView, UploadProfilePicture, UserDetailView, UserMeView, UserProfileUpdateView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('signin/', SigninView.as_view()),
    path('update/', UserProfileUpdateView.as_view()),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('upload-pfp/', UploadProfilePicture.as_view()),
]
