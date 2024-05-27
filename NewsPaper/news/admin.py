from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'author', 'created_date')
    list_filter = ('created_date', 'author', 'categories__name')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'categories__name')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)


