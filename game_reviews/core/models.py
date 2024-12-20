from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone


# User model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('critic', 'Critic'),
        ('user', 'User'),

    ]

    username = models.CharField(max_length=255, unique=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    publication = models.CharField(max_length=255, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='user')
    first_name = models.CharField(max_length=30, blank=True, null=True)  # Make it optional
    last_name = models.CharField(max_length=30, blank=True, null=True)  # Make it optional

    # Set the field used for authentication
    USERNAME_FIELD = 'username'  # This should be 'username' since you want to use it for login
    REQUIRED_FIELDS = ['email']  # You can add other fields required for creating superusers

    def __str__(self):
        return self.username


# Game model
from django.core.files.storage import default_storage


class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    developer = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    release_date = models.DateField()
    age_rating = models.IntegerField()
    image = models.ImageField(upload_to='games/images/', null=True, blank=True)  # For uploaded images
    video = models.FileField(upload_to='games/videos/', null=True, blank=True)  # For uploaded videos
    file = models.FileField(upload_to='games/files/', null=True, blank=True)  # For uploaded files
    platform = models.ManyToManyField('Platform', through='GamePlatform', blank=True)
    category = models.ManyToManyField('Category', through='GameCategory', blank=True)
    tags = models.ManyToManyField('Tag', through='GameTag', blank=True)
    steam_app_id = models.IntegerField(blank=True, null=True)
    parent_game = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    genre = models.TextField(max_length=255, default='empty')


    def __str__(self):
        return self.title

    def __str__(self):
        return self.title

    # Property to calculate the average rating for the game
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


# Comment model
class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.game.title}"


# Like model
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


# Review model
class Review(models.Model):
    comment = models.TextField()
    title = models.CharField(max_length=255)
    helpful_votes = models.IntegerField(null=True, blank=True, default=0)
    report_count = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Tag model
class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name


# Category model
class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


# Platform model
class Platform(models.Model):
    platform_name = models.CharField(max_length=255)

    def __str__(self):
        return self.platform_name


# Many-to-Many Relationships
class GameTag(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class GameCategory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class GamePlatform(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
