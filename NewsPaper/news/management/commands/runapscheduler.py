import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


from news.models import Category, Post


logger = logging.getLogger(__name__)


def my_job():
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


@util.close_old_connections
def delete_old_job_execution(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute='00', hour='18', day_of_week='FRI'),
            # trigger=CronTrigger(minute='49',hour='19'),
            id='my_job',
            max_instances=1,
            replace_existing=True
        )
        logger.info("Добавлено задание 'my_job'.")

        scheduler.add_job(
            delete_old_job_execution,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info('Старт scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Стоп scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')