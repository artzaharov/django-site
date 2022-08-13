from django.contrib import admin
from django.urls import path, include
from article.views import ArticleViewSet
from rest_framework import routers


# DRF routes
router = routers.SimpleRouter()
router.register(r'article', ArticleViewSet)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include(router.urls)),  # подключаем маршруты SimpleRouter
	path('api/v1/auth/', include('rest_framework.urls')),  # подключаем маршруты авторизации и аутентификации DRF
	path('', include('article.urls')),
]
