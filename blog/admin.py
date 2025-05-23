from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'verified', 'created_at')
    list_filter = ('verified', 'created_at')
    search_fields = ('title', 'content')
