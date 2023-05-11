from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from news.models import Post


@receiver(post_save, sender= Post)
def news_create(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(subscriptions__category = instance.postCategory).values_list('email', flat=True)
    subject = f'Новая статья в категории { instance.postCategory }'

    text_content = (
        f'Новость: { instance.title }\n'
        f'Ссылка на товар: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Новость: {instance.title}<br><br>',
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
