from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    
    url(r'^articles/(?P<article_slug>[\w-]+)/comments/?$', 
        views.CommentsListCreateAPIView.as_view()),

    url(r'^articles/(?P<article_slug>[\w-]+)/comments/(?P<comment_pk>[\d]+)/?$',
        views.CommentsDestroyAPIView.as_view()),
    
    url(r'^tags/?$', views.TagListAPIView.as_view()),
] 