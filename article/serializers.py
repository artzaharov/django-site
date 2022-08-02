from rest_framework import serializers
from .models import Article


# сериализатор привязанный к Модели
class ArticleSerializer(serializers.ModelSerializer):
	author = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = Article
		fields = ('title', 'slug', 'content', 'image', 'created_at', 'updated_at', 'views', 'is_published', 'category', 'tags', 'author')


# сериализатор прописанный вручную
# class ArticleSerializer(serializers.Serializer):
# 	title = serializers.CharField(max_length=255)
# 	slug = serializers.SlugField(max_length=255)
# 	content = serializers.CharField()
# 	image = serializers.ImageField()
# 	created_at = serializers.DateTimeField()
# 	updated_at = serializers.DateTimeField()
# 	views = serializers.IntegerField(default=0)
# 	is_published = serializers.BooleanField(default=True)
# 	category_id = serializers.IntegerField()
# 	tags = serializers.CharField()
# 	author_id = serializers.IntegerField()

# 	def create(self, validated_data):
# 		return Article.create(**validated_data)

# 	def update(self, instance, validated_data):
# 		instance.title = validated_data.get('title', instance.title)
# 		instance.save()
# 		return instance
