from django.urls import path

from news.views import PostsList, PostDetails, CreateNews, PostSearch, PostUpdate, NewsDelete

urlpatterns = [
    path('', PostsList.as_view(), name = 'post_list'),
    path('<int:pk>', PostDetails.as_view(), name = 'detail_news'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name = 'edit_news'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name = 'delete_news'),
    path('search/', PostSearch.as_view(), name = 'search_news'),
    path('create/', CreateNews.as_view(), name = 'add_news'),
]