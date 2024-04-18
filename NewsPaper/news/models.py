from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):  #Модель, содержащая объекты всех авторов.
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        postR = 0
        postR += postRat.get('postRating')

        commRat = self.user.comment_set.aggregate(commRating=Sum('rating'))
        commR = 0
        commR += commRat.get('commRating')

        self.rating = postR * 3 + commR
        self.save()


class Category(models.Model):  #Модель Категорий новостей/статей
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categoties', through='Subscription')

    def __str__(self):
        return self.name.title()


class Post(models.Model):  #Модель постов. Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    article = 'AR'
    news = 'NW'

    CHOICES = [
        ('article', 'Статья'),
        ('news', 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):  #Модель категории постов. Промежуточная модель для связи «многие ко многим»:
#связь «один ко многим» с моделью Post;
#связь «один ко многим» с моделью Category.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):  #Модель комментариев. Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )




