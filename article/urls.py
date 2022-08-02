from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
	path('', HomePage.as_view(), name='home'),
	path('article/<str:slug>/', ShowArticle.as_view(), name='article'),
	path('category/<str:slug>/', ArticlesByCategory.as_view(), name='category'),
	path('tag/<str:slug>/', ArticlesByTag.as_view(), name='tag'),
	path('addarticle/', AddArticle.as_view(), name='addarticle'),
	path('search/', SearchResults.as_view(), name='search'),
	path('login/', user_login, name='login'),
	path('logout/', user_logout, name='logout'),
	path('register/', register, name='register'),
	path('contacts/', Contacts.as_view(), name='contacts'),
	path('startparser/', start_parser, name='startparser'),
]

#  только на локалке
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
