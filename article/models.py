from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
	title = models.CharField(max_length=255, verbose_name='Название')
	slug = models.SlugField(max_length=255, verbose_name='ЧПУ', unique=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('category', kwargs={'slug': self.slug})

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
		ordering = ['title']


class Tag(models.Model):
	title = models.CharField(max_length=255, verbose_name='Название')
	slug = models.SlugField(max_length=255, verbose_name='ЧПУ', unique=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('tag', kwargs={'slug': self.slug})

	class Meta:
		verbose_name = 'Тег'
		verbose_name_plural = 'Теги'
		ordering = ['title']


class Article(models.Model):
	title = models.CharField(max_length=255, verbose_name='Название')
	slug = models.SlugField(max_length=255, verbose_name='ЧПУ', unique=True)
	content = models.TextField(blank=False, verbose_name='Текст')
	image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, verbose_name='Изображение')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
	views = models.IntegerField(default=0, verbose_name='Просмотров')
	is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
	category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='articles')
	tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги', related_name='articles')
	author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор', related_name='articles')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('article', kwargs={'slug': self.slug})

	class Meta:
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'
		ordering = ['-created_at']
