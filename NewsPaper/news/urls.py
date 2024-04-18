from django.urls import path, include
from django.views.decorators.cache import cache_page

# Импортируем созданные нами представления
from .views import PostList, PostDetail, Search, NewsCreate, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete, subscriptions

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60)(PostList.as_view()), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', (PostDetail.as_view()), name='post_detail'), #убрал cache_page(60*5)
   path('news/search/', Search.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path("accounts/", include("allauth.urls")),
   path('subscriptions/', subscriptions, name='subscriptions'),

]