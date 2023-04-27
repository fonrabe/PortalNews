from django.urls import path

from news.views import PostsList, PostDetails

urlpatterns = [
    path('', PostsList.as_view(), name = 'post_list'),
    path('<int:pk>', PostDetails.as_view()),
    # path('create/', CreateNews.as_view(), name = 'add_news'),
]