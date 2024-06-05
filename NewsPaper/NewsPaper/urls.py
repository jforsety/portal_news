from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (news/urls.py)
   # подключались к главному приложению с префиксом NewsPaper/.
   path('', include('news.urls')),
   path("accounts/", include("allauth.urls")),
]