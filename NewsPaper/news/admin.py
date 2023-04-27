from django.contrib import admin
from .models import Post, PostCategory, Category, Comment, Author

admin.site.register(Post)
admin.site.register(PostCategory)

