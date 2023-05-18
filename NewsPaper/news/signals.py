from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from news.models import Post
from news.tasks import send_createNews


@receiver(post_save, sender= Post)
def news_create(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(subscriptions__category = instance.postCategory).values_list('email', flat=True)
    send_createNews(instance, emails)