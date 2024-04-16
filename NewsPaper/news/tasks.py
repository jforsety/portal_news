import datetime
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post


@shared_task #рассылка уведомлений на email подписчиков о созданных за последние 7 дней новостях в подписанной категории
def weekly_send_email_task():
    today = datetime.datetime.today()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_date__gte=last_week)
    categories = posts.values_list('categories', flat=True)
    subscribers = User.objects.filter(subscriptions__category__in=categories).values_list('email', flat=True)
    subject = 'Сводка новостей за неделю'
    html = render_to_string(
        template_name='weekly_newsletter.html',
        context={
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(subject=subject, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html, 'text/html')
    msg.send()


@shared_task #рассылка уведомлений на email подписчиков при создании новости подписанной категории
def send_email_task(pk):
    post = Post.objects.get(pk=pk)  # определяем созданную новость по переданному pk
    subscribers_emails = User.objects.filter(subscriptions__category__in=post.categories.all()).values_list('email', flat=True)
    subject = f'Новый пост в категории: {[i for i in post.categories.all()]}'

    text = (
        f'Тип публикации: {post.type}'
        f'Автор: {post.author}'
        f'Название: {post.title}'
        f'Краткое содержание: {post.preview()}'
        f'Ссылка на публикацию: http://127.0.0.1:8000/{post.get_absolute_url()}'
    )

    html = (
        f'Тип публикации: {post.type}<br>'
        f'Автор: {post.author}<br>'
        f'Название: {post.title}'
        f'Краткое содержание: {post.preview()}'
        f'--<a href=http://127.0.0.1:8000/{post.get_absolute_url()}>Ссылка на публикацию</a>--<br><br>'
    )

    msg = EmailMultiAlternatives(subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers_emails)
    msg.attach_alternative(html, 'text/html')
    msg.send()