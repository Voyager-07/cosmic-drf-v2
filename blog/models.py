from django.db import models
from user.models import User
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    thumbnailurl = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    readtime = models.IntegerField()
    verified = models.BooleanField(default=False)
