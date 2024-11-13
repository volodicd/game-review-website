from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, GameForm
from .models import Game, Review
from .utils import get_game_info
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm


def home(request):
    latest_games = Game.objects.order_by('-id')[:10]  # Fetch the latest 10 games
    return render(request, 'core/home.html', {'latest_games': latest_games})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def account_details(request):
    return render(request, 'core/account_details.html', {'user': request.user})


@login_required
def critic_dashboard(request):
    if request.user.role != 'critic':
        return redirect('home')
    return render(request, 'core/critic_dashboard.html')


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    #steam_info = get_steam_info(game)  # Assuming you have this function
    reviews = game.reviews.all()  # Assuming the Game model has a related reviews field

    # Initialize the comment form
    comment_form = CommentForm()  # This creates an empty form

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.game = game
                new_comment.save()
                return redirect('game_detail', game_id=game.id)
        else:
            return redirect('login')

    context = {
        'game': game,
        #'steam_info': steam_info,
        'reviews': reviews,
        'comment_form': comment_form,  # Passing comment_form to the template
        #'error_message': 'Steam information not available' if not steam_info else None,
    }
    return render(request, 'core/game.html', context)


@login_required
def create_game(request):
    if not request.user.role == 'admin':  # Ensure only admins can access this view
        return HttpResponseForbidden("You are not authorized to create games.")

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after saving
    else:
        form = GameForm()

    return render(request, 'core/create_game.html', {'form': form})


@login_required
def edit_game(request, game_id):
    if not (request.user.role == 'admin' or request.user.role == 'moderator'):
        return HttpResponseForbidden("You are not authorized to edit games.")

    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm(instance=game)

    return render(request, 'core/edit_game.html', {'form': form, 'game': game})


@login_required
def delete_game(request, game_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to delete games.")

    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        game.delete()
        return redirect('home')  # Redirect to home after deletion

    return render(request, 'core/delete_game_confirm.html', {'game': game})

def game_list(request):
    games = Game.objects.all()  # Fetch all games from the database
    return render(request, 'core/game_list.html', {'games': games})

def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    #steam_info = get_steam_info(game)  # Assuming you have a method for this
    reviews = game.reviews.all()  # Assuming the Game model has a related reviews field

    # Initialize the comment form
    comment_form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.game = game
                new_comment.save()
                return redirect('game', game_id=game.id)
        else:
            # Handle unauthenticated users
            return redirect('login')

    context = {
        'game': game,
        #'steam_info': steam_info,
        'reviews': reviews,
        'comment_form': comment_form,
        #'error_message': 'Steam information not available' if not steam_info else None,
    }
    return render(request, 'core/game.html', context)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user is a moderator
    if request.user.role == 'moderator':
        comment.delete()
        return redirect('game_detail', game_id=comment.game.id)  # Redirect to the game page
    else:
        return HttpResponseForbidden("You don't have permission to delete this comment.")