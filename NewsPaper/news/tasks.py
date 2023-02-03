from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from .models import Post, article, news, Category, PostCategory


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def notify_subscribers(pid):
    new_post = Post.objects.get(pk=pid)
    sub_users = new_post.category.all().values('subscribers__email')
    cats = new_post.category.all().values('name')
    print(new_post)

    sub_males = [sub['subscribers__email'] for sub in sub_users]
    cat_name = [cat['name'] for cat in cats]

    html_content = render_to_string(
        'post_for_send.html',
        {
            'post': new_post,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{cat_name}: {new_post.heading}',
        body=new_post.text,
        from_email='lion4652@yandex.ru',
        to=sub_males,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()