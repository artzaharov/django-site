from django import template
from article.models import Category, Tag, Article
from django.db.models import Count, F


register = template.Library()


@register.simple_tag
def get_categories():
	categories = Category.objects.annotate(cnt=Count('articles', filter=F('articles__is_published'))).filter(cnt__gt=0)
	return categories


@register.simple_tag
def get_tags():
	tags = Tag.objects.annotate(cnt=Count('articles', filter=F('articles__is_published'))).filter(cnt__gt=0)
	return tags


@register.simple_tag
def get_popular():
	popular = Article.objects.order_by('-views')[:6]
	return popular
