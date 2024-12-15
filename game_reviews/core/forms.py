from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Game, Comment, Review


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image', 'description', 'publication', 'role']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'image': forms.URLInput(attrs={'placeholder': 'Profile Image URL'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'title', 'description', 'release_date', 'developer', 'publisher',
            'genre', 'image', 'video', 'file', 'steam_app_id', 'parent_game',
            'age_rating', 'platform', 'category', 'tags'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.SelectMultiple(),
            'category': forms.SelectMultiple(),
            'platform': forms.SelectMultiple(),
            'genre': forms.Textarea(attrs={'rows': 2, 'maxlength': '255'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'parent']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'parent': forms.HiddenInput(),  # Hide parent field if adding a reply
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        labels = {
            'rating': 'Your Rating',
            'comment': 'Review Comment',
            'title': 'Review Title',
        }
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Rating from 1 to 5
            'comment': forms.Textarea(attrs={'rows': 4}),
            'title': forms.TextInput(attrs={'placeholder': 'Review Title'}),
        }


class RoleChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']

    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('critic', 'Critic'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)


class FileUploadForm(forms.Form):
    file = forms.FileField(label="Choose a File")
