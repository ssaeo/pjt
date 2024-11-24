from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'profile_img')


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'user', 'comments_count', 'views')


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)
