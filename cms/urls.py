"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from article.views import ArticleAPIList, ArticleAPIDetails
from article.views import ArticleViewSet
from rest_framework import routers


# DRF routes
router = routers.SimpleRouter()
router.register(r'article', ArticleViewSet)  # 3-й параметр: basename='article' - для именования генерируемых маршрутов

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include(router.urls)),  # подключаем DRF маршруты SimpleRouter
	path('api/v1/auth/', include('rest_framework.urls')),  # подключаем маршруты авторизации и аутентификации DRF
	# path('api/v1/articlelist/', ArticleAPIList.as_view()),
	# path('api/v1/articlelist/<int:pk>/', ArticleAPIList.as_view()),
	# path('api/v1/articlelist/', ArticleViewSet.as_view({'get': 'list'})),  # DRF ViewSet route
	# path('api/v1/article/<int:pk>/', ArticleViewSet.as_view({'put': 'update'})),  # DRF ViewSet route
	# path('api/v1/articledetails/<int:pk>/', ArticleAPIDetails.as_view()),
	path('', include('article.urls')),
]
