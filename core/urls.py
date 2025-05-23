from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('api/user/', include('user.urls')),
    path('api/blog/', include('blog.urls')),
]
