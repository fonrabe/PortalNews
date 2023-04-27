from django.shortcuts import render
from django.views.generic import ListView, DetailView

from news.models import Post


class PostsList(ListView):
    model = Post
    ordering = '-dateCreate'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'