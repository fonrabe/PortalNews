from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .filters import PostFilter
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


class CreateNews(CreateView):
    pass


class PostSearch(ListView):
    model = Post
    ordering = '-dateCreate'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context