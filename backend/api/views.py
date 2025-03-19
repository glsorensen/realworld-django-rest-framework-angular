from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing article instances.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()
        author = self.request.query_params.get('author', None)
        tag = self.request.query_params.get('tag', None)
        favorited = self.request.query_params.get('favorited', None)
        
        if favorited is not None:
            queryset = queryset.filter(favorited_by__user__username=favorited)
        
        if author is not None:
            queryset = queryset.filter(author__user__username=author)
        
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)
            
        return queryset

    # Assume there are more methods here...
    # Let's add a placeholder for line 120 to match the PR patch
    def favorite(self, request, slug):
        # Placeholder implementation
        article = self.get_object()
        serializer_context = {'request': request}
        serializer = self.serializer_class(article, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def feed(self, request):
        """Get articles from users the current user follows"""
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated('Authentication required')
            
        user_profile = request.user.profile
        followed_users = user_profile.follows.all()
        queryset = Article.objects.filter(author__in=followed_users)
        
        page = self.paginate_queryset(queryset)
        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        
        return self.get_paginated_response(serializer.data)