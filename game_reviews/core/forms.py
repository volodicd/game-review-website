from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Game, Comment, Review

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')

class CustomUserEditForm(forms.ModelForm):  # Add this form for editing critic profiles
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image', 'description', 'publication']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'release_date', 'developer', 'genre', 'image_url', 'steam_app_id','parent_game']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Your Rating',
            'comment': 'Review Comment',
        }
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Rating from 1 to 5
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
