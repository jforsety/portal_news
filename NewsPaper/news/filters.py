from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, IsoDateTimeFilter
from .models import *


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    # Поиск по автору
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        empty_label='любой',
        label='Автор поста',
    )
    # Поиск по названию
    post_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название поста',
    )
    # Поиск по категории
    post_category = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        empty_label='любой',
        label='Категория',
        #conjoined=True,
    )
    # Поиск по дате
    date = IsoDateTimeFilter(
        field_name='created_date',
        lookup_expr='gt',
        label='Дата создания',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )

   # class Meta:
   #     # В Meta классе мы должны указать Django модель,
   #     # в которой будем фильтровать записи.
   #     model = Post
   #     # В fields мы описываем по каким полям модели
   #     # будет производиться фильтрация.
   #     fields = {
   #         # поиск по названию
   #         'title': ['icontains'],
   #         # количество товаров должно быть больше или равно
   #         'categories': ['exact'],
   #     }
