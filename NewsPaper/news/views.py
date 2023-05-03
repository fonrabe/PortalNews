from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from news.models import Post
from .forms import NewsForm
from django.urls import reverse_lazy


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


class CreateNews(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        print(post)
        return super().form_valid(form)


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


class PostUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class CreateArticle(CreateNews):
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')