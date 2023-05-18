from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from news.models import Post, Subscriber


@shared_task
def send_createNews(instance, subscribers):
    subject = f'Новая статья в категории {instance.postCategory}'
    text_content = (
        f'Новость: {instance.title}\n'
        f'Ссылка на товар: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Новость: {instance.title}<br><br>',
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in subscribers:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_every_weeks():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreate__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Subscriber.objects.filter(category_in=categories).values_list('user__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    for email in subscribers:
        msg = EmailMultiAlternatives(subject= 'Статьи за неделю',
                                     body= '',
                                     from_email= settings.DEFAULT_FROM_EMAIL,
                                     to= email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
