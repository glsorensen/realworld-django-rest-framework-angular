from django.db import models
from django.contrib.auth.models import User

class TimestampedModel(models.Model):
    # Created and edited timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class Article(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    body = models.TextField()
    # The author field should be a Foreign Key to Profile
    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='articles'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='articles'
    )

    def __str__(self):
        return self.title


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag


class Profile(TimestampedModel):
    # Link to User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    
    # A Profile can have many followers
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )
    
    # Users can favorite many Articles
    favorites = models.ManyToManyField(
        'articles.Article',
        related_name='favorited_by'
    )
    
    def __str__(self):
        return self.user.username
    
    def follow(self, profile):
        """Follow a profile if we're not already following it"""
        self.follows.add(profile)
        
    def unfollow(self, profile):
        """Unfollow a profile if we're already following it"""
        self.follows.remove(profile)
        
    def is_following(self, profile):
        """Return True if we are following the given profile; False otherwise"""
        return self.follows.filter(pk=profile.pk).exists()
        
    def favorite(self, article):
        """Favorite an article if we haven't already favorited it"""
        self.favorites.add(article)
        
    def unfavorite(self, article):
        """Unfavorite an article if we've already favorited it"""
        self.favorites.remove(article)
        
    def has_favorited(self, article):
        """Return True if user has favorited the article; False otherwise"""
        return self.favorites.filter(pk=article.pk).exists()