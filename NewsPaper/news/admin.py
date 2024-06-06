from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin
# импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'author', 'created_date')
    list_filter = ('created_date', 'author', 'categories__name')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'categories__name')  # тут всё очень похоже на фильтры из запросов в базу


# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin1(TranslationAdmin):
    model = Post

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)


