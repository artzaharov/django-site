import requests
from django.views.generic import ListView, DetailView, CreateView, FormView
from .models import *
from .forms import *
from django.http import Http404
from django.db.models import F
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from cms.settings import ARTICLES_PER_PAGE, MEDIA_ROOT
from bs4 import BeautifulSoup
from django.template.defaultfilters import slugify
from transliterate import translit
from datetime import datetime
from pathlib import os
from .serializers import ArticleSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView


class HomePage(ListView):
	model = Article
	extra_context = {'title': 'Главная'}
	paginate_by = ARTICLES_PER_PAGE

	def get_queryset(self):
		return Article.objects.filter(is_published=True).select_related('category', 'author')


class ArticlesByCategory(ListView):
	paginate_by = ARTICLES_PER_PAGE

	def get_queryset(self):
		return Article.objects.filter(category__slug=self.kwargs['slug'], is_published=True).select_related('category', 'author')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = Category.objects.get(slug=self.kwargs['slug'])
		return context


class ArticlesByTag(ListView):
	paginate_by = ARTICLES_PER_PAGE

	def get_queryset(self):
		return Article.objects.filter(tags__slug=self.kwargs['slug'], is_published=True).select_related('category', 'author')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
		return context


class ShowArticle(DetailView):
	model = Article

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = Article.objects.get(slug=self.kwargs['slug'])
		self.object.views = F('views') + 1
		self.object.save()
		self.object.refresh_from_db()
		return context


class AddArticle(LoginRequiredMixin, CreateView):
	model = Article
	form_class = AddArticleForm
	login_url = '/login/'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.author = self.request.user
		self.object.slug = slugify(translit(self.object.title, 'ru', reversed=True))
		self.object.is_published = False
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class SearchResults(ListView):
	paginate_by = ARTICLES_PER_PAGE

	def get_queryset(self):
		return Article.objects.filter(title__icontains=self.request.GET.get('s'), is_published=True).select_related('category', 'author')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Результаты поиска'
		context['s'] = f"s={self.request.GET.get('s')}&"
		return context


class Contacts(FormView):
	template_name = 'article/contacts.html'
	form_class = ContactForm
	success_url = '/contacts/'

	def form_valid(self, form):
		if form.send_email():
			messages.success(self.request, 'Сообщение успешно отправлено')
		else:
			messages.error(self.request, 'Ошибка отправки сообщения')
		return super().form_valid(form)


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Успешная регистрация')
			return redirect('home')
		else:
			messages.error(request, 'Ошибка регистрации')
	else:
		form = UserRegisterForm()

	return render(request, 'article/registering.html', {'form': form})


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'Ошибка входа')
	else:
		form = UserLoginForm()

	return render(request, 'article/login.html', {'form': form})


def user_logout(request):
	logout(request)
	return redirect('home')


def get_html(url):
	response = requests.get(url)
	return response.text


def get_data(html):
	soup = BeautifulSoup(html, 'lxml')

	try:
		title = soup.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').span.text.strip()
		slug = slugify(translit(title, 'ru', reversed=True))
	except Exception:
		title = ''
		slug = ''
	try:
		content = soup.find('div', class_='article-formatted-body').text.strip()
	except Exception:
		content = ''
	try:
		image = soup.find('div', class_='article-formatted-body').find('img').get('src')
	except Exception:
		image = ''

	data = {
		'title': title,
		'content': content,
		'slug': slug,
		'is_published': True,
		'category_id': 1,
		'image': image,
	}
	return data


def get_links(html):
	urls = []
	soup = BeautifulSoup(html, 'lxml')
	links = soup.find_all('a', class_='tm-article-snippet__title-link')
	for link in links:
		urls.append('https://habr.com' + link.get('href'))

	return urls


def image_downloader(img):
	img_name = img.split('/')[-1]
	current_date = datetime.now().strftime('%Y/%m/%d')
	img_folder = f'{MEDIA_ROOT}/images/{current_date}'

	if not os.path.exists(img_folder):
		try:
			os.makedirs(img_folder)
		except Exception:
			print('Невозможно создать папку')
			return ''

	img_path = f'{img_folder}/{img_name}'

	response = requests.get(img)
	with open(img_path, 'wb') as f:
		f.write(response.content)

	img_path = f'images/{current_date}/{img_name}'

	return img_path


def start_parser(request):
	if not request.user.is_superuser:
		raise Http404

	reports = []
	base_url = 'https://habr.com/ru/top/daily/'

	urls = get_links(get_html(base_url))

	for url in urls:
		data = get_data(get_html(url))
		article = Article.objects.filter(slug=data['slug']).exists()

		if article:
			reports.append('<span style="color:red;font-weight:bold">[ - ]</span> ' + data['title'])
		else:
			if data['image']:
				try:
					data['image'] = image_downloader(data['image'])
				except Exception:
					data['image'] = ''

			data['author'] = request.user
			Article.objects.create(**data)
			reports.append('<span style="color:green;font-weight:bold">[ + ]</span> ' + data['title'])

		form_data = {
			'reports': reports
		}

	return render(request, 'article/parser.html', form_data)


# DRF ViewSet - заменяет все отдельные DRF views, чтобы не дублировать код
class ArticleViewSet(ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer
	# даем доступ только прописанным категориям пользователей. Доступны 4 категории: AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
	permission_classes = (IsAuthenticatedOrReadOnly,)

	# переопределяем метод get_queryset и отдаем не все записи, а, например, только первые 3
	def get_queryset(self):
		pk = self.kwargs.get('pk')
		if not pk:
			return Article.objects.all()[:3]

		return Article.objects.filter(pk=pk)

	# с помощью декоратора @action добавляем произвольный маршрут (в данном примере - с категориями (выводит все категории), но может быть любой)
	@action(methods=['get'], detail=False)
	def category(self, request):
		cats = Category.objects.all()
		return Response({'cats': [c.title for c in cats]})


# DRF с привязкой к Модели

# получение всех записей
# class ArticleAPIList(ListCreateAPIView):
# 	queryset = Article.objects.all()
# 	serializer_class = ArticleSerializer


# # апдейт записи
# class ArticleAPIUpdate(UpdateAPIView):
# 	queryset = Article.objects.all()
# 	serializer_class = ArticleSerializer


# # класс позволяющий получать, обновлять и удалять запись
# class ArticleAPIDetails(RetrieveUpdateDestroyAPIView):
# 	queryset = Article.objects.all()
# 	serializer_class = ArticleSerializer


# ----------------------------------------------------

# DRF с определением всех методов вручную

# class ArticleAPI(APIView):
# 	def get(self, request):
# 		articles = Article.objects.all()
# 		return Response({'posts': ArticleSerializer(articles, many=True).data})

# 	def post(self, request):
# 		serializer = ArticleSerializer(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()
# 		return Response({'post': serializer.data})

# 	def put(self, request, *args, **kwargs):
# 		pk = kwargs.get('pk', None)
# 		if not pk:
# 			return Response({'error': 'Method PUT is not allowed'})

# 		try:
# 			instance = Article.objects.get(pk=pk)
# 		except Exception:
# 			return Response({'error': 'Object not found'})

# 		serializer = ArticleSerializer(data=request.data, instance=instance)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()
# 		return Response({'post': serializer.data})

# 	def delete():
# 		pk = kwargs.get('pk', None)
# 		if not pk:
# 			return Response({'error': 'Method DELETE is not allowed'})

# 		try:
# 			instance = Article.objects.get(pk=pk)
# 			instance.delete()
# 		except Exception:
# 			return Response({'error': 'Object not found'})
# 		return Response({'post': 'Deleted post: ' + str(pk)})
