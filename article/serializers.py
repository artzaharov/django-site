from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
	author = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = Article
		fields = ('title', 'slug', 'content', 'image', 'created_at', 'updated_at', 'views', 'is_published', 'category', 'tags', 'author')
