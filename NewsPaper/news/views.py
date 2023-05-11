from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from news.models import Post, Category, Subscriber
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef


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


class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
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


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.edit_post',)
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class CreateArticle(CreateNews):
    # permission_required = ('news.add_post',)
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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id= category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user= request.user, category= category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user= request.user, category= category).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed= Exists(
            Subscriber.objects.filter(user= request.user, category = OuterRef('pk'))
        )
    ).order_by('name')

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
