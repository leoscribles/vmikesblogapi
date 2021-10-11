from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from django.contrib.auth.models import User
from dj_rest_auth.models import TokenModel

from .models import Category, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = TokenModel
        fields = ('key', 'user',)

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user

class CustomUserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ('pk', 'email', 'username', 'password',)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.CharField()
    class Meta:
        model = Post
        fields = ('id','category_id', 'title', 'body', 'featured_image', 'created_at',)

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post_id = serializers.CharField()
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'name', 'body', 'created_at',)

