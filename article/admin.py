from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


class ArticleAdmin(admin.ModelAdmin):
	verbose_name = 'Статья'
	verbose_name_plural = 'Статьи'
	prepopulated_fields = {"slug": ("title",)}
	list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'author', 'views', 'is_published')
	list_display_links = ('id', 'title')
	list_editable = ('is_published',)
	list_filter = ('category', 'author', 'is_published')
	search_fields = ('title', 'content')
	fields = ('title', 'slug', 'category', 'author', 'content', 'tags', 'get_image', 'image', 'views', 'created_at', 'updated_at', 'is_published')
	readonly_fields = ('views', 'created_at', 'updated_at', 'get_image')
	save_on_top = True
	save_as = True

	def get_image(self, obj):
		if obj.image:
			return mark_safe(f'<img src="{obj.image.url}" width="100">')
		return '-'

	get_image.short_description = 'Текущее изображение'


class CategoryAdmin(admin.ModelAdmin):
	verbose_name = 'Категория'
	verbose_name_plural = 'Категории'
	prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
	verbose_name = 'Тег'
	verbose_name_plural = 'Теги'
	prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
