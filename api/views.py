from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer, CommentSerializer
from .models import Post, Comment, Category
from rest_framework.permissions import IsAuthenticated

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    print('queryset: ')
    print(queryset)
    serializer_class = PostSerializer
    print('PostSerializer: ')
    print(PostSerializer)
    # permission_classes = [IsAuthenticated]
    # print('permission_classes: ')
    # print(permission_classes)

    def __str__(self):
        return self.queryset + ' - ' + self.serializer_class

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

