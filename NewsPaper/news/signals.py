# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
# from .models import PostCategory
#
#
# @receiver(signal=m2m_changed, sender=PostCategory)
# def post_created(instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.categories.all()
#         users = User.objects.filter(subscriptions__category__in=categories).distinct()
#
#         emails = [user.email for user in users]
#
#         subject = f'Новый пост в категории: {[i for i in instance.categories.all()]}'
#
#         text = (
#             f'Тип публикации: {instance.type}'
#             f'Автор: {instance.author}'
#             f'Название: {instance.title}'
#             f'Краткое содержание: {instance.preview()}'
#             f'Ссылка на публикацию: http://127.0.0.1:8000/{instance.get_absolute_url()}'
#         )
#
#         html = (
#             f'Тип публикации: {instance.type}<br>'
#             f'Автор: {instance.author}<br>'
#             f'Название: {instance.title}'
#             f'Краткое содержание: {instance.preview()}'
#             f'--<a href=http://127.0.0.1:8000/{instance.get_absolute_url()}>Ссылка на публикацию</a>--<br><br>'
#         )
#
#         msg = EmailMultiAlternatives(subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=emails)
#         msg.attach_alternative(html, 'text/html')
#         msg.send()
#Закоментил чтобы отрабатывали таски Celery