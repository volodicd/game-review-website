from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('critic', 'Critic'),
        ('user', 'User'),

    ]

    # Role assigned to the user, determining permissions and access
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Profile image for critics
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # Description field for critics to share their background or specialties
    description = models.TextField(blank=True, null=True)

    # The publication or affiliation of the critic
    publication = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    # Property to check if the user is a critic
    @property
    def is_critic(self):
        return self.role == 'critic'


class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    developer = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    steam_app_id = models.IntegerField(blank=True, null=True)  # Added by your friend

    def __str__(self):
        return self.title

    # Property to calculate the average rating for the game
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')  # Link to Game model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to CustomUser
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()  # Review comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for review creation

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating}/5)"


class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.game.title}'
